# Django Imports
from django.urls import path

# Account Service Imports
from account_service.views import (
    RegisterAPIView, 
    LoginAPIView, 
    RefreshLoginAPIView,
    LogoutAPIView,
    VerifyEmailAPIView,
    VerifyEmailUidTokenAPIView 
)

app_name = "account_service"

urlpatterns = [
    path("register/", RegisterAPIView.as_view(), name="register"),
    path("login/", LoginAPIView.as_view(), name="login"),
    path("login/refresh/", RefreshLoginAPIView.as_view(), name="login_refresh"),
    path("logout/", LogoutAPIView.as_view(), name="logout"),
    
    path("verify_email/", VerifyEmailAPIView.as_view(), name="verify_email"),
    path("verify_email/<uidb64>/<token>/", VerifyEmailUidTokenAPIView.as_view(), name="verify_uidb64_token")
]
