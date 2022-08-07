# Django Imports
from django.urls import path

# Account Service Imports
from account_service.views import (
    RegisterAPIView, 
    LoginAPIView, 
    RefreshLoginAPIView
)  

urlpatterns = [
    path("register/", RegisterAPIView.as_view(), name="register"),
    path("login/", LoginAPIView.as_view(), name="login"),
    path("login/refresh/", RefreshLoginAPIView.as_view(), name="login_refresh"),
]
