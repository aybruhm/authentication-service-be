# Django Imports
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static

# DRF YASG Imports
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Rest Framework Imports
from rest_framework import permissions


# Schema Definition
schema_view = get_schema_view(
   openapi.Info(
      title="Authentication Service Backend",
      default_version='v1',
      description="Handles storage of users and authentication of their identities.",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="israelvictory87@gmail.com"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
   path("admin/", admin.site.urls),
   
   # api version 1 routes
   path("api/v1/", include("authentication_service.urls")),
   
   # api documentation routes
   re_path(r'^generate_api_docs(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
   re_path(r'^docs/swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='api_docs_swagger'),
   re_path(r'^docs/redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='api_docs_redoc'),
]

if settings.DEBUG:
   urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)