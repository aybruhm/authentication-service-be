# Django Imports
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpRequest
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

# Types Imports
from typing import NoReturn

# Accounts Imports
from authentication_service.models import AccountUser



def send_email_to_user(request: HttpRequest, user:AccountUser, uid:str, token:str) -> NoReturn:
    
    current_site = get_current_site(request)
    mail_subject = '[Loopscentral]: Verify Your Email'
    
    email_context = {
        'user': user,
        'domain': current_site.domain,
        'uid': uid,
        'token': token,
    }
    
    # Parse html to string
    html_content = render_to_string('emails/verify-email-template.html', email_context)
    text_content = strip_tags(html_content)

    # # Initialize a single email message which can be send to multiple recipients
    msg = EmailMultiAlternatives(mail_subject, text_content, settings.DEFAULT_FROM_EMAIL, [user.email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def send_reset_password_email_to_user(request: HttpRequest, user:AccountUser, uid:str, token:str) -> NoReturn:
    
    current_site = get_current_site(request)
    mail_subject = '[Loopscentral]: Reset Your Password'
    
    email_context = {
        'user': user,
        'domain': current_site.domain,
        'uid': uid,
        'token': token,
    }
    
    # Parse html to string
    html_content = render_to_string('emails/reset-password-email-template.html', email_context)
    text_content = strip_tags(html_content)
    
    # # Initialize a single email message which can be send to multiple recipients
    msg = EmailMultiAlternatives(mail_subject, text_content, settings.DEFAULT_FROM_EMAIL, [user.email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
