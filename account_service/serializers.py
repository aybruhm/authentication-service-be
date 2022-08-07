# Rest Framework Imports
from rest_framework import serializers

# SimpleJWT Imports
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

# Account Service Imports
from account_service.models import AccountUser

# Third Party Imports
from rest_api_payload import success_response


class RegisterUserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = AccountUser
        fields = ("username", "email", "password")
        extra_kwargs = {
            "password": {"write_only": True},
            "email": {"write_only": True},
        }
        
    def create(self, validated_data) -> AccountUser:
        
        # get fields from validated data
        username = validated_data.get("username")
        email = validated_data.get("email")
        password = validated_data.get("password")
        
        # create user
        user = AccountUser.objects.create(
            username=username,
            email=email,
            password=password
        )
        user.set_password(password)
        user.save()
        
        return user
    
    
class UserLoginObtainPairSerializer(TokenObtainPairSerializer):
    
    def validate(self, attrs):
        """The default result (access/refresh tokens)"""
        data = super(UserLoginObtainPairSerializer, self).validate(attrs)

        """Custom data you want to include"""
        data.update({"username": self.user.username})
        data.update({"email": self.user.email})
        data.update({"id": self.user.id})

        """Return custom data in the response"""
        payload = success_response(
            status="success", message="Login successful", data=data
        )
        return payload
    

class UserEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    
    
class UserResetPasswordSerializer(serializers.Serializer):
    new_password = serializers.Serializer(required=True)
    repeat_new_password = serializers.Serializer(required=True)