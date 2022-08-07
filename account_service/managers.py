from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    use_in_migrations: bool = True
    
    def create_user(
        self,
        email: str,
        username: str,
        password=None,
    ):
        """Creates normal user"""

        if email is None:
            raise TypeError("Users must have an email address")

        if username is None:
            raise TypeError("User must have a username")

        user = self.model(
            firstname="",
            lastname="",
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

        if firstname is None:
            raise TypeError("Admin must have a firstname")

        if lastname is None:
            raise TypeError("Admin must have a lastname")

        if email is None:
            raise TypeError("Admin must have an email address")

        if password is None:
            raise TypeError("Superusers must have a password.")

        user = self.create_user(
            email=email,
            username=username,
            password=password,
        )
        user.firstname = firstname
        user.lastname = firstname
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.save()

        return user