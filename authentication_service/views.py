# Rest Framework Imports
from rest_framework import status, views, permissions
from rest_framework.response import Response
from rest_framework.request import Request

# Djang Imports
from django.contrib.auth import logout, hashers
from django.conf import settings
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
        """
        The function creates a user, generates a verification link, 
        and sends an email to the user.
        
        :param request: The request object
        :type request: Request
        :return: A response object with a payload of data and a status code.
        """
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            
            # get password from validated data
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
        """
        It logs out the user and returns a 204 status code
        
        :param request: This is the request object that is passed to the view
        :type request: Request
        :return: A response object with a status code of 204 and no content.
        """
        logout(request)
        payload = success_response(status=True, message="Logged out successful!", data={})
        return Response(data=payload, status=status.HTTP_204_NO_CONTENT)
    
    
class RequestEmailUidTokenAPIView(views.APIView):
    permission_classes = (permissions.AllowAny, )
    serializer_class = UserEmailSerializer
    
    @swagger_auto_schema(request_body=UserEmailSerializer)
    def post(self, request:Request) -> Response:
        """
        It takes in a request object, validates the email address, 
        gets the inactive user, generates a
        uid and token, and sends an email to the user.
        
        :param request: The request object
        :type request: Request
        :return: A response object with a payload of data and a status code.
        """
        
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
                status=True, 
                message="An email activation link has been sent to your mail inbox!",
                data={}
            )
            return Response(data=payload, status=status.HTTP_202_ACCEPTED)

        payload = error_response(status=False, message=serializer.errors)
        return Response(data=payload, status=status.HTTP_400_BAD_REQUEST)
    

class VerifyEmailUidTokenAPIView(views.APIView):
    permission_classes = (permissions.AllowAny, )
    
    def post(self, request:Request, uidb64, token) -> Response:
        """
        It takes in a uidb64 and token, decodes the uidb64, 
        gets the user with the uid, checks if the
        token is valid, and if it is, 
        sets the user's is_email_active and is_active to True.
        
        :param request: The request object
        :type request: Request
        :param uidb64: The base64 encoded uuid of the user
        :param token: The token generated by the default_token_generator
        :return: A response object with a payload of data and a status code.
        """
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = AccountUser._default_manager.get(uuid=uid)
            
        except(TypeError, ValueError, OverflowError, AccountUser.DoesNotExist):
            user = None
            
        if user is not None and default_token_generator.check_token(user, token):
            user.is_email_active = True
            user.is_active = True
            user.save(update_fields=["is_email_active", "is_active"])
            
            payload = success_response(
                status=True,
                message="Email activated!",
                data={}
            )
            return Response(data=payload, status=status.HTTP_202_ACCEPTED)
        
        payload = error_response(status=False, message="Email activation link is invalid. Request again!")
        return Response(data=payload, status=status.HTTP_400_BAD_REQUEST)
    

class ResetPasswordAPIView(views.APIView):
    permission_classes = (permissions.AllowAny, )
    serializer_class = UserEmailSerializer
    
    @swagger_auto_schema(request_body=UserEmailSerializer)
    def post(self, request:Request) -> Response:
        """
        It takes in a request object, 
        validates the email address, 
        generates a uid and token, and sends
        an email to the user.
        
        :param request: The request object
        :type request: Request
        :return: A response object with a payload of data and a status code.
        """
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            
            user = get_active_user(
                request=request, 
                email=serializer.validated_data.get("email")
            )
        
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
        
        payload = error_response(status=False, message=serializer.errors)
        return Response(data=payload, status=status.HTTP_400_BAD_REQUEST)
    

class VerifyResetPasswordUidToken(views.APIView):
    permission_classes = (permissions.AllowAny, )
    serializer_class = UserResetPasswordSerializer
    
    def get(self, request:Request, uidb64, token) -> Response:
        """
        It takes a uidb64 and token, 
        decodes the uidb64, 
        and checks if the token is valid for the user
        
        :param request: The request object
        :type request: Request
        :param uidb64: The base64 encoded uuid of the user
        :param token: The token generated by the default_token_generator
        :return: A response object with a payload of data and a status code.
        """
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
        """
        The function takes in a request, 
        decodes the base64 encoded user id, 
        gets the user with the id,
        sets the user's password to the new password, 
        and saves the user to the database.
        
        :param request: The request object that was sent to the view
        :type request: Request
        :param uidb64: The base64 encoded user id
        :param token: The token that was sent to the user's email
        :return: A response object with a payload of data and a status code.
        """
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            new_password = serializer.validated_data.get("new_password")
            re_new_password = serializer.validated_data.get("repeat_new_password")
            
            if new_password != re_new_password:
                payload = error_response(status=False, message="Password incorrect. Please try again!")
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
        """
        If the current password is correct, 
        and the new password equals the repeat new password,
        update the user password and save to database
        
        :param request: This is the request object that is sent to the API
        :type request: Request
        :return: A response object with a payload of data and a status code.
        """
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
                user.save(update_fields=["password"])

            
            payload = success_response(
                status=True, 
                message="Password changed successfully!",
                data={}
            )
            return Response(data=payload, status=status.HTTP_202_ACCEPTED)
        
        payload = error_response(status=False, message=serializer.errors)
        return Response(data=payload, status=status.HTTP_400_BAD_REQUEST)
    

class SuspendUserAPIView(views.APIView):
    permission_classes = (CanSuspendUserPermission, )
    
    def put(self, request:Request, user_email:str) -> Response:
        """
        This function suspends a user
        
        :param request: The request object
        :type request: Request
        :param user_email: The email of the user to be suspended
        :type user_email: str
        :return: A response object with a payload of data and a status code.
        """
        user = get_active_user(request=request, email=user_email)
        
        if user is not None:
            user.is_suspended = True
            user.save(update_fields=["is_suspended"])
            
            payload = success_response(
                status=True,
                message="User has been suspended!",
                data={}
            )
            return Response(data=payload, status=status.HTTP_202_ACCEPTED)
        
        payload = error_response(status=False, message="User account is not activated.")
        return Response(data=payload, status=status.HTTP_400_BAD_REQUEST)
    
    
class GoogleOAuth2LoginAPIView(views.APIView):
    serializer_class = GoogleOAuth2Serializer
    
    @swagger_auto_schema(request_body=GoogleOAuth2Serializer)
    def post(self, request:Request, *args, **kwargs) -> Response:
        """
        We are validating the id_token that is sent in the header of the request. 
        
        If the id_token is valid, we are creating a response object and then calling the jwt_login
        function
        
        :param request: This is the request object that is sent to the server
        :type request: Request
        :return: The response object is being returned.
        """
        
        # The above code is validating the id_token 
        # that is sent in the header of the request.
        id_token = request.headers.get('id_token')
        google_validate_id_token(id_token=id_token)
    
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        # We use get-or-create logic here for the sake of the example.
        # We don't have a sign-up flow.
        user, _ = user_get_or_create(**serializer.validated_data)

        # The above code is creating a response object and 
        # then calling the jwt_login function.
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
        'site_name': settings.AUTHENTICATION_SERVICE["site_name"],
        'contact_email': settings.AUTHENTICATION_SERVICE["contact_email"]
    }
    return render(request, "emails/verify-email-template.html", email_context)


def reset_password_email_template(request: HttpRequest) -> HttpResponse:
    email_context = {
        'user': request.user,
        'domain': "http://" + request.get_host(),
        'uid': "6sbcshbcsk9=ec-eckem",
        'token': "wh8xHhbUbyGvBYBUBNm",
        'contact_email': settings.AUTHENTICATION_SERVICE["contact_email"]
    }
    return render(request, "emails/reset-password-email-template.html", email_context)