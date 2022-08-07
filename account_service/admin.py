# Django Imports
from django.contrib import admin
from django.conf import settings

# Account Service Imports
from account_service.models import User


# register user if set in the settings, otherwise don't.
if settings.REGISTER_USER_MODEL:
    
    @admin.register(User)
    class UserAdmin(admin.ModelAdmin):
        list_display = ("id", "firstname", "lastname", "email", "username")
        list_filter = ("id", "email", "username")