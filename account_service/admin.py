# Django Imports
from django.contrib import admin
from django.conf import settings

# Account Service Imports
from account_service.models import AccountUser


# register user if set in the settings, otherwise don't.
if settings.REGISTER_USER_MODEL:
    
    @admin.register(AccountUser)
    class AccountUserAdmin(admin.ModelAdmin):
        list_display = (
            "id", "uuid", "firstname", "lastname", 
            "email", "username", "is_active", "is_email_active", 
            "is_suspended", 
        )
        list_filter = ("id", "email", "username")