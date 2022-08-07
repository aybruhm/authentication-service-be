# Rest Framework Imports
from rest_framework import status, views, permissions
from rest_framework.response import Response
from rest_framework.request import Request

# Djang Imports
from django.contrib.auth import logout

# SimpleJWT Imports
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.serializers import TokenRefreshSerializer

# Account Service Imports
from account_service.serializers import (
    RegisterUserSerializer,
    UserLoginObtainPairSerializer,
    UserEmailSerializer
)
from account_service.services.emails.users import send_email_to_user
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
    
    def post(self, request:Request) -> Response:
        serializer = RegisterUserSerializer(data=request.data)
        
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
    
    def post(self, request:Request) -> Response:
        
        serializer = UserEmailSerializer(data=request.data)
        
        if serializer.is_valid():
            
            # get inactive user
            user = get_inactive_user(email=serializer.validated_data.get("email"))
            
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