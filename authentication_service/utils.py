# Rest Framework Imports
from rest_framework.request import Request

# Django Imports
from django.db.models import Q

# Account Service Imports
from authentication_service.models import AccountUser


def get_inactive_user(request:Request, email:str):
    """
    This function returns the user with the given email if the user is inactive
    
    :param request: This is the request object that is passed to the view
    :type request: Request
    :param email: The email address of the user you want to get
    :type email: str
    :return: The user object is being returned.
    """
    
    user = AccountUser.objects.filter(
        Q(email__iexact=email) & Q(is_active=False)  
    ).first()
    return user
    

def get_active_user(request:Request, email:str):
    """
    This function returns an active user with the given email address
    
    :param request: This is the request object that is passed to the view
    :type request: Request
    :param email: The email address of the user
    :type email: str
    :return: The user object
    """
    
    user = AccountUser.objects.filter(
        Q(email__iexact=email) & Q(is_active=True)  
    ).first()
    return user