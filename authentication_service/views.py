# Rest Framework Imports
from rest_framework import status, views, permissions
from rest_framework.response import Response
from rest_framework.request import Request

# Djang Imports
from django.contrib.auth import logout, hashers
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

# DRF YASG Imports
from drf_yasg.utils import swagger_auto_schema

# SimpleJWT Imports
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from authentication_service.models import AccountUser
from authentication_service.permissions import CanSuspendUserPermission

# Account Service Imports
from authentication_service.serializers import (
    RegisterUserSerializer,
    UserLoginObtainPairSerializer,
    UserEmailSerializer,
    UserResetPasswordSerializer,
    UserChangePasswordSerializer,
    GoogleOAuth2Serializer
)
from authentication_service.services.emails.users import (
    send_email_to_user, 
    send_reset_password_email_to_user
)
from authentication_service.services.generators.uid import generate_uid_token
from authentication_service.services.oauth2.google import google_validate_id_token
from authentication_service.services.oauth2.jwt import jwt_login
from authentication_service.services.users.records import user_get_me, user_get_or_create
from authentication_service.utils import (
    get_active_user, 
    get_inactive_user
)

# Third Party Imports
from rest_api_payload import success_response, error_response


class RegisterAPIView(views.APIView):
    serializer_class = RegisterUserSerializer
    permission_classes = [permissions.AllowAny]
    
    @swagger_auto_schema(request_body=RegisterUserSerializer)
    def post(self, request:Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            
            # get passowrd from validated data
            password = serializer.validated_data.get("password")
            
            # create user
            user = AccountUser.objects.create(**serializer.validated_data)
            user.set_password(password)
            user.save()
            
            # generate verification link for user
            uid, token = generate_uid_token(request=request, user=user)
            
            # send email to user
            if uid and token:
                send_email_to_user(request=request, user=user, uid=uid, token=token)
            
            payload = success_response(
                status=True, message="User created!",
                data=serializer.data
            )
            return Response(data=payload, status=status.HTTP_201_CREATED)
        
        payload = error_response(
            status=False, message=serializer.errors
        )
        return Response(data=payload, status=status.HTTP_400_BAD_REQUEST)
    

class LoginAPIView(TokenObtainPairView):
    """Inherits TokenObtainPairView from rest_framework simplejwt"""

    serializer_class = UserLoginObtainPairSerializer



class RefreshLoginAPIView(TokenRefreshView):
    """Inherits TokenRefreshView from rest_framework simplejwt"""

    serializer_class = TokenRefreshSerializer
    
    
class LogoutAPIView(views.APIView):
    permission_classes = (permissions.IsAuthenticated, )
    
    def post(self, request:Request) -> Response:
        request.session.flush()
        logout(request)

        payload = success_response(status=True, message="Logged out successful!", data={})
        return Response(data=payload, status=status.HTTP_204_NO_CONTENT)
    
    
class VerifyEmailAPIView(views.APIView):
    permission_classes = (permissions.AllowAny, )
    serializer_class = UserEmailSerializer
    
    @swagger_auto_schema(request_body=UserEmailSerializer)
    def post(self, request:Request) -> Response:
        
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            
            # get inactive user
            user = get_inactive_user(request=request, email=serializer.validated_data.get("email"))
            print("USER: ", user)
            
            # generate verification link for user
            uid, token = generate_uid_token(request=request, user=user)
            
            # send email to user if uid and token is generated
            if uid and token:
                send_email_to_user(request=request, user=user, uid=uid, token=token)
            
            payload = success_response(
                status=True, message="An email activation link has been sent to your mail inbox!",
                data={}
            )
            return Response(data=payload, status=status.HTTP_202_ACCEPTED)

        payload = error_response(
            status=False,
            message=serializer.errors
        )
        return Response(data=payload, status=status.HTTP_400_BAD_REQUEST)
    

class VerifyEmailUidTokenAPIView(views.APIView):
    permission_classes = (permissions.AllowAny, )
    
    def post(self, request:Request, uidb64, token) -> Response:
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = AccountUser._default_manager.get(uuid=uid)
            
        except(TypeError, ValueError, OverflowError, AccountUser.DoesNotExist):
            user = None
            
        if user is not None and default_token_generator.check_token(user, token):
            user.is_email_active = True
            user.is_active = True
            user.save()
            
            payload = success_response(
                status=True,
                message="Email activated!",
                data={}
            )
            return Response(data=payload, status=status.HTTP_202_ACCEPTED)
        
        payload = error_response(
            status=False, message="Email activation link is invalid. Request again!"
        )
        return Response(data=payload, status=status.HTTP_400_BAD_REQUEST)
    

class ResetPasswordAPIView(views.APIView):
    permission_classes = (permissions.AllowAny, )
    serializer_class = UserEmailSerializer
    
    @swagger_auto_schema(request_body=UserEmailSerializer)
    def post(self, request:Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            
            user = get_active_user(request=request, email=serializer.validated_data.get("email"))
        
            # generate verification link for user
            uid, token = generate_uid_token(request=request, user=user)
            
            # send email to user
            if uid and token:
                send_reset_password_email_to_user(request=request, user=user, uid=uid, token=token)
            
            payload = success_response(
                status=True,
                message="Password reset link has been sent to your mail inbox!",
                data={}
            )
            return Response(data=payload, status=status.HTTP_202_ACCEPTED)
        
        payload = error_response(
            status=False, message=serializer.errors
        )
        return Response(data=payload, status=status.HTTP_400_BAD_REQUEST)
    

class VerifyResetPasswordUidToken(views.APIView):
    permission_classes = (permissions.AllowAny, )
    serializer_class = UserResetPasswordSerializer
    
    def get(self, request:Request, uidb64, token) -> Response:
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = AccountUser._default_manager.get(uuid=uid)
            
        except(TypeError, ValueError, OverflowError, AccountUser.DoesNotExist):
            user = None
        
        if user is not None and default_token_generator.check_token(user, token):
            payload = success_response(
                status=True,
                message="Password reset link verified!",
                data={}
            )
            return Response(data=payload, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(request_body=UserResetPasswordSerializer)
    def post(self, request:Request, uidb64, token) -> Response:
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            new_password = serializer.validated_data.get("new_password")
            re_new_password = serializer.validated_data.get("repeat_new_password")
            
            if new_password != re_new_password:
                payload = error_response(
                    status=False,
                    message="Password(s) are incorrect. Please try again!"
                )
                return Response(data=payload, status=status.HTTP_400_BAD_REQUEST)
            
            # Decoding base64 to get user id
            uid = urlsafe_base64_decode(uidb64).decode()
            
            # Get first user with id
            user = AccountUser.objects.filter(uuid=uid).first()
            
            # Update user password and save to database
            user.set_password(new_password)
            user.save()
            
            payload = success_response(
                status=True,
                message="Password successfully changed!",
                data={}
            )
            return Response(data=payload, status=status.HTTP_202_ACCEPTED)
        
    
class ChangePasswordAPIView(views.APIView):
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = UserChangePasswordSerializer
    
    @swagger_auto_schema(request_body=UserChangePasswordSerializer)
    def put(self, request:Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            
            user = get_active_user(request=request, email=serializer.validated_data.get("email"))
            current_password = serializer.validated_data.get("current_password")
            new_password = serializer.validated_data.get("new_password")
            repeat_new_password = serializer.validated_data.get("repeat_new_password")
            
            # Confirms if the current inputted password equals to the user password
            can_change_password = (
                True
                if hashers.check_password(current_password, user.password)
                else False
            )

            # If can_change_password is True, 
            # and new password requals the repeat new password, 
            # set the password message to True else False
            password_message = (
                True
                if can_change_password is True and new_password == repeat_new_password
                else False
            )
            
            # Update user password and save to database
            if password_message is True:
                user.password = new_password
                user.set_password(new_password)
                user.save()

            
            payload = success_response(
                status=True, message="Password changed successfully!",
                data={}
            )
            return Response(data=payload, status=status.HTTP_202_ACCEPTED)
        
        payload = error_response(
            status=False, message=serializer.errors
        )
        return Response(data=payload, status=status.HTTP_400_BAD_REQUEST)
    

class SuspendUserAPIView(views.APIView):
    permission_classes = (CanSuspendUserPermission, )
    
    def put(self, request:Request, user_email:str) -> Response:
        user = get_active_user(request=request, email=user_email)
        
        if user:
            user.is_suspended = True
            user.save()
            
            payload = success_response(
                status=True,
                message="User has been suspended!",
                data={}
            )
        
        return Response(data=payload, status=status.HTTP_202_ACCEPTED)
    
    
class GoogleOAuth2LoginAPIView(views.APIView):
    serializer_class = GoogleOAuth2Serializer
    
    @swagger_auto_schema(request_body=GoogleOAuth2Serializer)
    def post(self, request:Request, *args, **kwargs) -> Response:
        
        id_token = request.headers.get('id_token')
        google_validate_id_token(id_token=id_token)
        
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        # We use get-or-create logic here for the sake of the example.
        # We don't have a sign-up flow.
        user, _ = user_get_or_create(**serializer.validated_data)

        response = Response(data=user_get_me(user=user))
        response = jwt_login(response=response, user=user)

        return response

    
# Email Template Views
def verify_email_template(request: HttpRequest) -> HttpResponse:
    email_context = {
        'user': request.user,
        'domain': "http://" + request.get_host(),
        'uid': "6sbcshbcsk9=ec-eckem",
        'token': "wh8xHhbUbyGvBYBUBNm",
    }
    return render(request, "emails/verify-email-template.html", email_context)


def reset_password_email_template(request: HttpRequest) -> HttpResponse:
    email_context = {
        'user': request.user,
        'domain': "http://" + request.get_host(),
        'uid': "6sbcshbcsk9=ec-eckem",
        'token': "wh8xHhbUbyGvBYBUBNm",
    }
    return render(request, "emails/reset-password-email-template.html", email_context)