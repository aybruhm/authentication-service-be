from typing import List
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin


class User(AbstractBaseUser, PermissionsMixin):
    # Primary Key
    id = models.BigAutoField(primary_key=True, unique=True)
    
    # Basic information
    firstname = models.CharField(max_length=255, help_text="What's your firstname?", blank=True, null=True)
    lastname = models.CharField(max_length=255, help_text="What's your lastname?", blank=True, null=True)
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
    REQUIRED_FIELDS: List[str] = ["username", "email"]
    
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
        return "{} {}".format(self.firstname, self.lastname)
    
    def is_user_active(self) -> bool:
        if self.is_active:
            return True
        return False
    
    def fullname(self) -> str:
        return "{} {}".format(self.firstname, self.lastname)