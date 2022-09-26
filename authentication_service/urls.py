# Django Imports
from django.urls import path

# Account Service Imports
from authentication_service.views import (
    RegisterAPIView, 
    LoginAPIView, 
    RefreshLoginAPIView,
    LogoutAPIView,
    RequestEmailUidTokenAPIView,
    VerifyEmailUidTokenAPIView,
    ResetPasswordAPIView, 
    VerifyResetPasswordUidToken,
    ChangePasswordAPIView,
    SuspendUserAPIView,
    GoogleOAuth2LoginAPIView,
    
    verify_email_template,
    reset_password_email_template
)

app_name = "authentication_service"

urlpatterns = [
    # main auth
    path("register/", RegisterAPIView.as_view(), name="register"),
    path("login/", LoginAPIView.as_view(), name="login"),
    path("login/refresh/", RefreshLoginAPIView.as_view(), name="login_refresh"),
    path("google_oauth2_login/", GoogleOAuth2LoginAPIView.as_view(), name="google_oauth2_login"),
    path("logout/", LogoutAPIView.as_view(), name="logout"),
    
    # verify email
    path("request_email_uid_token/", RequestEmailUidTokenAPIView.as_view(), name="request_email_token"),
    path("verify_email/<uidb64>/<token>/", VerifyEmailUidTokenAPIView.as_view(), name="verify_uidb64_token"),
    
    # reset password
    path("reset_password/", ResetPasswordAPIView.as_view(), name="reset_password"),
    path("reset_password/<uidb64>/<token>/", VerifyResetPasswordUidToken.as_view(), name="reset_uidb64_token"),
    
    # change password
    path("change_password/", ChangePasswordAPIView.as_view(), name="change_password"),
    
    # suspend user
    path("suspend_user/<str:user_email>/", SuspendUserAPIView.as_view(), name="suspend_user"),
    
    # Email Template URLs
    path("verify_email_template/", verify_email_template),
    path("reset_password_email_template/", reset_password_email_template)
]
