# Rest Framework Imports
from rest_framework import status, views, permissions
from rest_framework.response import Response
from rest_framework.request import Request

# Djang Imports
from django.contrib.auth import logout, hashers
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode

# DRF YASG Imports
from drf_yasg.utils import swagger_auto_schema

# SimpleJWT Imports
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from account_service.models import AccountUser

# Account Service Imports
from account_service.serializers import (
    RegisterUserSerializer,
    UserLoginObtainPairSerializer,
    UserEmailSerializer,
    UserResetPasswordSerializer,
    UserChangePasswordSerializer
)
from account_service.services.emails.users import (
    send_email_to_user, 
    send_reset_password_email_to_user
)
from account_service.services.generators.uid import generate_uid_token
from account_service.utils import (
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
            serializer.save()
            
            payload = success_response(
                status="success", message="User created",
                data=serializer.data
            )
            return Response(data=payload, status=status.HTTP_201_CREATED)
        
        payload = error_response(
            status="error", message=serializer.errors
        )
        return Response(data=payload, status=status.HTTP_400_BAD_REQUEST)
    

class LoginAPIView(TokenObtainPairView):
    """Inherits TokenObtainPairView from rest_framework simplejwt"""

    serializer_class = UserLoginObtainPairSerializer



class RefreshLoginAPIView(TokenRefreshView):
    """Inherits TokenRefreshView from rest_framework simplejwt"""

    serializer_class = TokenRefreshSerializer
    
    
class LogoutAPIView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request:Request) -> Response:
        request.session.flush()
        logout(request)

        payload = success_response(status="success", message="Logged out successful!", data={})
        return Response(data=payload, status=status.HTTP_204_NO_CONTENT)
    
    
class VerifyEmailAPIView(views.APIView):
    permission_classes = (permissions.AllowAny)
    serializer_class = UserEmailSerializer
    
    @swagger_auto_schema(request_body=UserEmailSerializer)
    def post(self, request:Request) -> Response:
        
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            
            # get inactive user
            user = get_inactive_user(request=request, email=serializer.validated_data.get("email"))
            
            # generate verification link for user
            uid, token = generate_uid_token(request=request, user=user)
            
            # send email to user if uid and token is generated
            if uid and token:
                send_email_to_user(request=request, user=user, uid=uid, token=token)
            
            payload = success_response(
                status="success", message="An email activation link has been sent to your mail inbox!"
            )
            return Response(data=payload, status=status.HTTP_202_ACCEPTED)

        payload = error_response(
            status="error",
            message=serializer.errors
        )
        return Response(data=payload, status=status.HTTP_400_BAD_REQUEST)
    

class VerifyEmailUidTokenAPIView(views.APIView):
    permission_classes = (permissions.AllowAny)
    
    def post(self, request:Request, uidb64, token) -> Response:
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = AccountUser._default_manager.get(pk=uid)
            
        except(TypeError, ValueError, OverflowError, AccountUser.DoesNotExist):
            user = None
            
        if user is not None and default_token_generator.check_token(user, token):
            user.is_email_active = True
            user.is_active = True
            user.save()
            
            payload = success_response(
                status="success",
                message="Email activated!",
                data={}
            )
            return Response(data=payload, status=status.HTTP_202_ACCEPTED)
        
        payload = error_response(
            status="error", message="Email activation link is invalid. Request again!"
        )
        return Response(data=payload, status=status.HTTP_400_BAD_REQUEST)
    

class ResetPasswordAPIView(views.APIView):
    permission_classes = (permissions.AllowAny)
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
                status="success",
                message="Password reset link has been sent to your mail inbox!",
                data={}
            )
            return Response(data=payload, status=status.HTTP_202_ACCEPTED)
        
        payload = error_response(
            data=payload, message=serializer.errors
        )
        return Response(data=payload, status=status.HTTP_400_BAD_REQUEST)
    

class VerifyResetPasswordUidToken(views.APIView):
    permission_classes = (permissions.IsAuthenticated)
    serializer_class = UserResetPasswordSerializer
    
    def get(self, request:Request, uidb64, token) -> Response:
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = AccountUser._default_manager.get(pk=uid)
            
        except(TypeError, ValueError, OverflowError, AccountUser.DoesNotExist):
            user = None
        
        if user is not None and default_token_generator.check_token(user, token):
            payload = success_response(
                status="success",
                message="Password reset link verified!"
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
                    status="error",
                    message="Password(s) are incorrect. Please try again!"
                )
                return Response(data=payload, status=status.HTTP_400_BAD_REQUEST)
            
            # Decoding base64 to get user id
            uid = urlsafe_base64_decode(uidb64).decode()
            
            # Get first user with id
            user = AccountUser.objects.filter(id=uid).first()
            
            # Update user password and save to database
            user.set_password(new_password)
            user.save()
            
            payload = success_response(
                status="success",
                message="Password successfully changed!",
                data={}
            )
            return Response(data=payload, status=status.HTTP_202_ACCEPTED)
        
    
class ChangePasswordAPIView(views.APIView):
    permission_classes = (permissions.IsAuthenticated)
    serializer_class = UserChangePasswordSerializer
    
    @swagger_auto_schema(request_body=UserChangePasswordSerializer)
    def put(self, request:Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            
            user = get_active_user(request=request, user=serializer.validated_data.get("email"))
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
                status="success", message="Password changed successfully!",
                data={}
            )
            return Response(data=payload, status=status.HTTP_202_ACCEPTED)
        
        payload = error_response(
            status="error", message=serializer.errors
        )
        return Response(data=payload, status=status.HTTP_400_BAD_REQUEST)