# Django Imports
from django.http import HttpRequest
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode

# Accounts Imports
from authentication_service.models import AccountUser


def generate_uid_token(request:HttpRequest, user:AccountUser):
    
    # generate a safe base64 encoded url
    uid = urlsafe_base64_encode(force_bytes(user.uuid))
    
    # generate a token
    token = default_token_generator.make_token(user)
    
    return uid, token