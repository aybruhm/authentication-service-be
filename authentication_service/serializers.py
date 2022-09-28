# Rest Framework Imports
from rest_framework import serializers

# Django Imports
from django.db.models import Q

# SimpleJWT Imports
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

# Account Service Imports
from authentication_service.models import AccountUser

# Third Party Imports
from rest_api_payload import success_response, error_response


class RegisterUserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = AccountUser
        fields = ("firstname", "lastname", "username", "email", "password")
        extra_kwargs = {
            "password": {"write_only": True},
        }
        
    def validate(self, attrs):
        
        # Get email and username from attrs
        email = attrs.get("email")
        username = attrs.get("username")
        
        # Check if a user with the username or email exists
        if AccountUser.objects.filter(
            Q(email__iexact=email) | Q(username__iexact=username)  
        ).exists():
            raise serializers.ValidationError("User exits. Please try again!")
        
        return super().validate(attrs)
    
    
class UserLoginObtainPairSerializer(TokenObtainPairSerializer):
    
    def validate(self, attrs):
        """The default result (access/refresh tokens)"""
        data = super(UserLoginObtainPairSerializer, self).validate(attrs)
        
        # check if user is not active
        if self.user.is_active is False:
            
            payload = error_response(
                status=False,
                message="Account not activated. Kindly request for an activation link."
            )
            return payload
        
        # check if user is suspended
        if self.user.is_suspended is True:
            
            payload = success_response(
                status=True,
                message="Account suspended. Kindly reach out to the support team.",
                data={}
            )
            return payload

        # Added custom data to token serializer
        data.update({"firstname": self.user.firstname})
        data.update({"lastname": self.user.lastname})
        data.update({"username": self.user.username})
        data.update({"email": self.user.email})
        data.update({"id": self.user.id})

        payload = success_response(
            status=True, 
            message="Login successful", 
            data=data
        )
        return payload
    

class UserEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    
    def validate(self, attrs):
        
        # Get email from attrs
        email = attrs.get("email")
        
        # Check if a user with the email does not exist
        if not AccountUser.objects.filter(
                Q(email__iexact=email)
            ).exists():
            raise serializers.ValidationError("User does not exist.")
        
        return super().validate(attrs)
    
    
class UserResetPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(
        write_only=True,
        required=True,
        style={"input_type": "password", "placeholder": "New Password"},
    )
    repeat_new_password = serializers.CharField(
        write_only=True,
        required=True,
        style={"input_type": "password", "placeholder": "Repeat New Password"},
    )
    
    def validate(self, attrs):
        
        # get password (new and repeat) from attrs
        new_password = attrs.get("new_password")
        re_new_password = attrs.get("repeat_new_password")
        
        # Check if both password are not equal
        if new_password != re_new_password:
            raise serializers.ValidationError(
                {"incorrect_pwd": "Password incorrect. Please try again!"}
            )
        
        return super().validate(attrs)
    

class UserChangePasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    current_password = serializers.CharField(
        write_only=True,
        required=True,
        style={"input_type": "password", "placeholder": "Current Password"},
    )
    new_password = serializers.CharField(
        write_only=True,
        required=True,
        style={"input_type": "password", "placeholder": "New Password"},
    )
    repeat_new_password = serializers.CharField(
        write_only=True,
        required=True,
        style={"input_type": "password", "placeholder": "Repeat New Password"},
    )
    
    def validate(self, attrs):
        
        # Get email and pwds from attrs
        email = attrs.get("email")
        new_password = attrs.get("new_password")
        re_new_password = attrs.get("repeat_new_password")
        
        # Check if a user with the email does not exist
        if not AccountUser.objects.filter(
                Q(email__iexact=email)
            ).exists():
            raise serializers.ValidationError("User does not exist.")

        # Check if both password are not equal
        if new_password != re_new_password:
            raise serializers.ValidationError(
                {"incorrect_pwd": "Password incorrect. Please try again!"}
            )
        
        return super().validate(attrs)
    

class GoogleOAuth2Serializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(required=False, default='')
    last_name = serializers.CharField(required=False, default='')