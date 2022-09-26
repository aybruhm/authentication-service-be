# Django Imports
from django.urls import reverse

# Rest Framework Imports
from rest_framework.test import APIClient, APITestCase
from rest_framework import status

# Simple JWT Imports
from rest_framework_simplejwt.tokens import RefreshToken

# Own Imports
from authentication_service.models import AccountUser

# Native Imports
import json


# initialize api client
client = APIClient()


class BaseTestCase(APITestCase):
    
    def setUp(self) -> None:
        self.active_user = AccountUser.objects.get_or_create(
            firstname = "Abraham",
            lastname = "Israel",
            username = "israelabraham",
            email = "israelabraham@email.com",
            password = "someawfully_strongpassword_2022",
            is_active = True
        )[0]
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
        self.valid_email_payload = {
            "email": "israelabraham@email.com"
        }
        self.invalid_email_payload = {
            "email": "victory@email.com"
        }
        self.valid_pwd_payload = {
            "email": "israelabraham@email.com",
            "current_password": "someawfully_strongpassword_2022",
            "new_password": "someincredibly_awful_strong_password022",
            "repeat_new_password": "someincredibly_awful_strong_password022"
        }
        self.invalid_pwd_payload = {
            "email": "israelabraham@email.com",
            "current_password": "",
            "new_password": "someincredibly_awful_strong_password022"
        }
        
    @property
    def bearer_token(self):
        """
        Get access token for user
        """
        user = AccountUser.objects.get(email="israelabraham@email.com")
        refresh = RefreshToken.for_user(user)
        return {"HTTP_AUTHORIZATION": f"Bearer {refresh.access_token}"}
    

class RegisterTestCase(BaseTestCase):
    """Test case to register user"""
    
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
        

class VerifyEmailTestCase(BaseTestCase):
    
    def test_valid_verify_email(self):
        
        url = reverse("authentication_service:verify_email")
        response = client.post(url, data=self.valid_email_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        
    def test_invalid_verify_email(self):
        
        url = reverse("authentication_service:verify_email")
        response = client.post(url, data=self.invalid_email_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_valid_verify_email_uid_token(self):
        return ...
    
    def test_invalid_verify_email_uid_token(self):
        return ...
        

class ResetPasswordTestCase(BaseTestCase):
    
    def test_valid_reset_password(self):
        
        url = reverse("authentication_service:reset_password")
        response = client.post(url, data=self.valid_email_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
    
    def test_invalid_reset_password(self):
        
        url = reverse("authentication_service:reset_password")
        response = client.post(url, data=self.invalid_email_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_vaild_verify_reset_password_uid_token(self):
        return ...
    
    def test_invalid_verify_reset_password_uid_token(self):
        return ...
    
    
class ChangePasswordTestCase(BaseTestCase):
    
    def test_valid_change_password(self):
        
        url = reverse("authentication_service:change_password")
        response = client.put(url, data=self.valid_pwd_payload, format="json", **self.bearer_token)
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
    
    def test_invalid_change_password(self):
        url = reverse("authentication_service:change_password")
        response = client.put(url, data=self.invalid_pwd_payload, format="json", **self.bearer_token)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    
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