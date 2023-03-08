from django.urls import path, include,re_path
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from drf_project.views import HomeView

from drf_yasg.views import get_schema_view
from drf_yasg import openapi
#from django.conf.urls import url
from rest_framework import permissions
from drf_yasg.views import get_schema_view
# For swagger
schema_view = get_schema_view(
    openapi.Info(
        title="Crawler Swagger",
        default_version="first version",
        description="Docs for crawler manager",
        # terms_of_service="https://www.google.com/policies/terms/",
        # contact=openapi.Contact(name="test", email="test@test.com"),
        # license=openapi.License(name="Test License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns= [
    re_path(r'^(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]