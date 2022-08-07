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
    UserLoginObtainPairSerializer
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
    