# Django Imports
from django.contrib.auth.models import BaseUserManager
from django.db import transaction


class UserManager(BaseUserManager):
    use_in_migrations: bool = True
    
    def create_user(
        self,
        firstname: str,
        lastname: str,
        email: str,
        username: str,
        password=None,
    ):
        """Creates normal user"""
        
        if firstname is None:
            raise TypeError("User must have a firstname")
        
        if lastname is None:
            raise TypeError("User must have a last name")

        if email is None:
            raise TypeError("User must have an email address")

        if username is None:
            raise TypeError("User must have a username")

        user = self.model(
            firstname=firstname,
            lastname=lastname,
            username=username,
            email=self.normalize_email(email),
            phone_number="",
        )
        user.set_password(password)
        user.save()

        return user

    def create_superuser(
        self,
        firstname: str,
        lastname: str,
        username: str,
        email: str,
        password=None,
    ):
        """Creates super user"""

        if email is None:
            raise TypeError("Admin must have an email address")

        if password is None:
            raise TypeError("Superusers must have a password.")

        with transaction.atomic():
            user = self.create_user(
                firstname=firstname,
                lastname=lastname,
                email=email,
                username=username,
                password=password,
            )
            user.is_superuser = True
            user.is_staff = True
            user.is_active = True
            user.save()

            return user