# Django Imports
from django.urls import path

# Account Service Imports
from account_service.views import (
    RegisterAPIView, 
    LoginAPIView, 
    RefreshLoginAPIView,
    LogoutAPIView,
    VerifyEmailAPIView,
    VerifyEmailUidTokenAPIView,
    ResetPasswordAPIView, 
    VerifyResetPasswordUidToken,
    ChangePasswordAPIView
)

app_name = "account_service"

urlpatterns = [
    # main auth
    path("register/", RegisterAPIView.as_view(), name="register"),
    path("login/", LoginAPIView.as_view(), name="login"),
    path("login/refresh/", RefreshLoginAPIView.as_view(), name="login_refresh"),
    path("logout/", LogoutAPIView.as_view(), name="logout"),
    
    # verify email
    path("verify_email/", VerifyEmailAPIView.as_view(), name="verify_email"),
    path("verify_email/<uidb64>/<token>/", VerifyEmailUidTokenAPIView.as_view(), name="verify_uidb64_token"),
    
    # reset password
    path("reset_password/", ResetPasswordAPIView.as_view(), name="reset_password"),
    path("reset_password/<uidb64>/<token>/", VerifyResetPasswordUidToken.as_view(), name="reset_uidb64_token"),
    
    # change password
    path("change_password/", ChangePasswordAPIView.as_view(), name="change_password"),
]
