# Rest Framework Imports
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

# Account Service Imports
from authentication_service.models import AccountUser

# Third Party Imports
from rest_api_payload import error_response


def get_inactive_user(request:Request, email:str):
    
    try:
        user = AccountUser.objects.filter(email=email).first()
        return user
    except (AccountUser.DoesNotExist, Exception):
        payload = error_response(
            status="error",
            message="User does not exist!"
        )
        return Response(data=payload, status=status.HTTP_400_BAD_REQUEST)
    

def get_active_user(request:Request, email:str):
    
    try:
        user = AccountUser.objects.filter(email=email, is_active=True).first()
        return user
    except (AccountUser.DoesNotExist, Exception):
        payload = error_response(
            status="error",
            message="User does not exist!"
        )
        return Response(data=payload, status=status.HTTP_400_BAD_REQUEST)