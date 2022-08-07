# Rest Framework Imports
from rest_framework import serializers

# Account Service Imports
from account_service.models import AccountUser


class RegisterUserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = AccountUser
        fields = ("username", "email", "password")
        
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