# Django Imports
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode

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
    """
    The class is a subclass of the APITestCase class.
    """
    
    def setUp(self) -> None:
        # active and inactive user
        self.active_user = AccountUser.objects.get_or_create(
            firstname = "Abraham",
            lastname = "Israel",
            username = "israelabraham",
            email = "israelabraham@email.com",
            password = "someawfully_strongpassword_2022",
            is_active = True,
            is_staff = True
        )[0]
        self.inactive_user = AccountUser.objects.get_or_create(
            firstname = "Dan",
            lastname = "Odin",
            username = "danodin",
            email = "dpoxo@email.com",
            password = "someawfully_strongpassword_2022"
        )[0]
        
        # valid and invalid payload
        self.valid_payload = {
            "firstname": "Victory",
            "lastname": "Abraham",
            "username": "abram",
            "email": "abraham@email.com",
            "password": "someawfully_strongpassword_2022"
        }
        self.invalid_payload = {
            "firstname": "Abraham",
            "lastname": "Israel",
            "username": "",
            "email": "",
            "password": "someawfully_strongpassword_2022"
        }
        
        # valid and invalid email payload
        self.valid_email_payload = {
            "email": "dpoxo@email.com"
        }
        self.invalid_email_payload = {
            "email": "victory@email.com"
        }
        
        # valid and invalid password payload
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
        
        # valid and invalid reset password payload
        self.valid_reset_password_payload = {
            "new_password": "some_1234_incredible_5678_strongpwd",
            "repeat_new_password": "some_1234_incredible_5678_strongpwd"
        }
        self.invalid_reset_password_payload = {
            "new_password": "some_1234_incredible_5678_strongpwd",
            "repeat_new_password": "some_1234_incredible_56789091"
        }
        
    @property
    def bearer_token(self):
        """
        Get access token for user
        """
        user = AccountUser.objects.get(email="israelabraham@email.com")
        refresh = RefreshToken.for_user(user)
        return {"HTTP_AUTHORIZATION": f"Bearer {refresh.access_token}"}
    
    
    @property
    def generate_uid_token(self):
        """
        Get base64 encoded url, and token for user
        """
        
        user = AccountUser.objects.get(email="dpoxo@email.com")
        uid = urlsafe_base64_encode(force_bytes(user.uuid))
        token = default_token_generator.make_token(user)
        
        return uid, token
    

class RegisterTestCase(BaseTestCase):
    """
    Test case to register user
    """
    
    def test_valid_register(self):
        """
        Test case to ensure we can create a new user object.
        """
        url = reverse("authentication_service:register")
        response = client.post(url, data=self.valid_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    
    def test_invalid_register(self):
        """
        Test case to ensurue we can't create 
        a new user object with invalid data.
        """
        url = reverse("authentication_service:register")
        response = client.post(url, data=self.invalid_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        

class RequestVerifyEmailTestCase(BaseTestCase):
    """
    Test case to request / verify a user email address
    """
    
    def test_valid_request_email_uid_token(self):
        """
        Test case to ensure that the user can 
        request an activation link for their account 
        with the valid payload.
        """
        
        url = reverse("authentication_service:request_email_token")
        response = client.post(url, data=self.valid_email_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        
    def test_invalid_request_email_uid_token(self):
        """
        Test case to ensure that the user cannot 
        request an activation liink for their account
        with an invalid payload.
        """
        
        url = reverse("authentication_service:request_email_token")
        response = client.post(url, data=self.invalid_email_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_valid_verify_email_uid_token(self):
        """
        Test case to ensure that the user can 
        verify their account with the valid 
        uid and token.
        """
        
        uid, token = self.generate_uid_token
        url = reverse("authentication_service:verify_uidb64_token", args=[uid, token])
        
        response = client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(response.data, {"status": True, "message": "Email activated!", "data": {}})
    
    def test_invalid_verify_email_uid_token(self):
        """
        Test case to ensure that user cannot verify
        their account with an invalid uid and token.
        """
        
        uid, token = self.generate_uid_token
        url = reverse("authentication_service:verify_uidb64_token", args=[uid, token + "somerandome12322"])
        
        response = client.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        

class ResetPasswordTestCase(BaseTestCase):
    """
    Test case to reset a user password
    """
    
    def test_valid_reset_password(self):
        """
        Test case to ensure that the user can
        reset their password with a valid payload.
        """
        
        # update inactive user
        self.inactive_user.is_active = True
        self.inactive_user.save()
        
        url = reverse("authentication_service:reset_password")
        response = client.post(url, data=self.valid_email_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
    
    def test_invalid_reset_password(self):
        """
        Test case to ensure that the user cannot
        reset their password with an invalid payload.
        """
        
        url = reverse("authentication_service:reset_password")
        response = client.post(url, data=self.invalid_email_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_get_vaild_verify_reset_password_uid_token(self):
       
        uid, token = self.generate_uid_token
        url = reverse("authentication_service:reset_uidb64_token", args=[uid, token])
        
        response = client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"status": True, "message": "Password reset link verified!", "data": {}})
    
    def test_get_invalid_verify_reset_password_uid_token(self):
        
        uid, token = self.generate_uid_token
        url = reverse("authentication_service:reset_uidb64_token", args=[uid, token + "somerando242"])
        
        response = client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"status": False, "message": "Password reset link invalid!"})
    
    def test_post_vaild_verify_reset_password_uid_token(self):
        
        uid, token = self.generate_uid_token
        url = reverse("authentication_service:reset_uidb64_token", args=[uid, token])
        
        response = client.post(url, data=self.valid_reset_password_payload, format="json")
        
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(response.data, {"status": True, "message": "Password successfully changed!", "data": {}})
    
    def test_post_invalid_verify_reset_password_uid_token(self):
        
        uid, token = self.generate_uid_token
        url = reverse("authentication_service:reset_uidb64_token", args=[uid, token])
        
        response = client.post(url, data=self.invalid_reset_password_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    
class ChangePasswordTestCase(BaseTestCase):
    """
    Test case to change a user password
    """
    
    def test_valid_change_password(self):
        """
        Test case to ensure that the user can 
        change their password with a valid payload.
        """
        
        url = reverse("authentication_service:change_password")
        response = client.put(url, data=self.valid_pwd_payload, format="json", **self.bearer_token)
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
    
    def test_invalid_change_password(self):
        """
        Test case to ensure that the user cannot
        change their password with an invalid payload.
        """
        url = reverse("authentication_service:change_password")
        response = client.put(url, data=self.invalid_pwd_payload, format="json", **self.bearer_token)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    
class SuspendUserTestCase(BaseTestCase):
    """
    Test case to suspend a user account
    """
    
    def test_valid_suspend_user(self):
        """
        Test case to suspend a user.
        """
        
        # update inactive user
        self.inactive_user.is_active = True
        self.inactive_user.save()
        
        url = reverse("authentication_service:suspend_user", args=["dpoxo@email.com"])
        response = client.put(url, **self.bearer_token)
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        
    def test_invalid_suspend_user(self):
        """
        Test case to ensure that a user cannot
        suspend a user with a wrong email address.
        """
        
        url = reverse("authentication_service:suspend_user", args=["abram@email.in"])
        response = client.put(url, **self.bearer_token)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    
class GoogleOAuthLoginTestCase(BaseTestCase):
    
    def test_google_oauth_login(self):
        return ...