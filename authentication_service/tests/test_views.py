# Django Imports
from unittest import TestResult
from django.urls import reverse

# Rest Framework Imports
from rest_framework.test import APIClient, APITestCase
from rest_framework import status

# Simple JWT Imports
from rest_framework_simplejwt.tokens import RefreshToken

# Own Imports
from authentication_service.models import AccountUser


# initialize api client
client = APIClient()


class RegisterTestCase(APITestCase):
    """Test case to register user"""
    
    def setUp(self) -> None:
        self.valid_payload = {
            "firstname": "Abraham",
            "lastname": "Israel",
            "username": "abram",
            "email": "abram@email.com",
            "password": "someawfully_strongpassword_2022"
        }
        self.invalid_payload = {
            "firstname": "Abraham",
            "lastname": "Israel",
            "username": "",
            "email": "",
            "password": "someawfully_strongpassword_2022"
        }
    
    def test_valid_register(self):
        """
        Ensure we can create a new user object.
        """
        url = reverse("authentication_service:register")
        response = client.post(url, data=self.valid_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    
    def test_invalid_register(self):
        """
        Ensure we can't create a new user object with invalid data.
        """
        url = reverse("authentication_service:register")
        response = client.post(url, data=self.invalid_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        

class LoginTestCase(APITestCase):
    
    def setUp(self) -> None:
        self.user = AccountUser.objects.get_or_create(
            firstname = "Abraham",
            lastname = "Israel",
            username = "abram",
            email = "abram@email.com",
            password = "someawfully_strongpassword_2022"
        )[0]
        self.valid_payload = {
            "email": "abram@email.com",
            "password": "someawfully_strongpassword_2022"
        }
        self.invalid_payload = {
            "email": "hello@email.com",
            "password": "someawfully_strongpassword_2022"
        }
        
    # @property
    # def bearer_token(self):
    #     """
    #     Get access token for user
    #     """
    #     user = AccountUser.objects.get(email="abram@email.com")
    #     refresh = RefreshToken.for_user(user)
    #     return refresh.access_token
        
    # def test_valid_login(self):
        
    #     url = reverse("authentication_service:login")
    #     response = client.post(url, data=self.valid_payload, format="json")
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    # def test_invalid_login(self):
        
    #     url = reverse("authentication_service:login")
    #     response = client.post(url, data=self.invalid_payload, format="json")
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    # def test_valid_login_refresh(self):
        
    #     url = reverse("authentication_service:login_refresh")
    #     response = client.post(url, data={"refresh": self.bearer_token}, format="json")
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    

class ResetPasswordTestCase(APITestCase):
    
    def setUp(self) -> None:
        return super().setUp()
    
    def test_valid_reset_password(self):
        return ...
    
    def test_invalid_reset_password(self):
        return ...
    
    def test_vaild_verify_reset_password_uid_token(self):
        return ...
    
    def test_invalid_verify_reset_password_uid_token(self):
        return ...
    
    
class ChangePasswordTestCase(APITestCase):
    
    def setUp(self) -> None:
        return super().setUp()
    
    def test_valid_change_password(self):
        return ...
    
    def test_invalid_change_password(self):
        return ...
    
    
class SuspendUserTestCase(APITestCase):
    
    def setUp(self) -> None:
        return super().setUp()
    
    def test_valid_suspend_user(self):
        return ...
    
    def test_invalid_suspend_user(self):
        return ...
    
    
class GoogleOAuthLoginTestCase(APITestCase):
    
    def test_google_oauth_login(self):
        return ...