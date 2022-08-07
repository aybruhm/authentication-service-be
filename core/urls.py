# Django Imports
from django.contrib import admin
from django.urls import path, include, re_path

# DRF YASG Imports
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Rest Framework Imports
from rest_framework import permissions


# Schema Definition
schema_view = get_schema_view(
   openapi.Info(
      title="Loopscentral Internal Account Service API",
      default_version='v1',
      description="Authentication service backend apis for loopscentral platform",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="loopscentraltech@gmail.com"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include("account_service.urls")),
    
    # API Documentation Routes
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]