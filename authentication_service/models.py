# Typing Imports
from typing import List, Any
from uuid import uuid4

# Django Imports
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, 
    PermissionsMixin, 
)

# Account Service Imports
from authentication_service.managers import UserManager


class AccountUser(AbstractBaseUser, PermissionsMixin):
    # Primary Key
    id = models.BigAutoField(primary_key=True, unique=True)
    uuid = models.UUIDField(default=uuid4, unique=True, editable=False)
    
    # Basic information
    firstname = models.CharField(max_length=255, help_text="What's your firstname?", blank=True, null=True)
    lastname = models.CharField(max_length=255, help_text="What's your lastname?", blank=True, null=True)
    
    # Required basic information
    username = models.CharField(max_length=255, help_text="What's your preferred username?", unique=True)
    email = models.EmailField(max_length=255, help_text="What's your email address?", unique=True)
    
    # Meta information
    phone_number = models.CharField(max_length=255, help_text="What's your phone number?", blank=True, null=True)
    profile_picture = models.ImageField(upload_to="user_images/", blank=True, null=True)
    
    # Additional information
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_suspended = models.BooleanField(default=False)
    is_email_active = models.BooleanField(default=False)
    
    # Timestamp information
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS: List[str] = ["firstname", "lastname", "username"]
    
    objects: Any = UserManager()
    
    class Meta:
        verbose_name_plural = "users"
        db_table = "users"
        permissions = [
            ("can_suspend_user", "Can suspend user"),
        ]
        indexes = [
            models.Index(fields=[
                "username", "email", "is_active", 
                "date_created", "date_modified"
            ])
        ]
        
    def __str__(self) -> str:
        return self.username
    
    def fullname(self) -> str:
        return f"{self.firstname} {self.lastname}"