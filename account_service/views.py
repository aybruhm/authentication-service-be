# Rest Framework Imports
from rest_framework import status, views
from rest_framework.response import Response
from rest_framework.request import Request

# Account Service Imports
from account_service.serializers import (
    RegisterUserSerializer
)

# Third Party Imports
from rest_api_payload import success_response, error_response


class RegisterAPIView(views.APIView):
    serializer_class = RegisterUserSerializer
    
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