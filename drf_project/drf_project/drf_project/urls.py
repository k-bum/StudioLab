''' """drf_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path("admin/", admin.site.urls),
    
    #DRF
    path('api-auth/',include('rest_framework.urls'))
]
 '''
 
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

# Routers provide an easy way of automatically determining the URL conf.
# router = routers.DefaultRouter()
# router.register(r'users', UserViewSet)
schema_view = get_schema_view( 
    openapi.Info( 
        title="Swagger Study API", 
        default_version="v1", 
        description="Swagger Study를 위한 API 문서", 
        terms_of_service="https://www.google.com/policies/terms/", 
        contact=openapi.Contact(name="test", email="test@test.com"), 
        license=openapi.License(name="Test License"), 
    ), 
    public=True, 
    permission_classes=(permissions.AllowAny,), 
)

urlpatterns = [
    #path('', include(router.urls)),
    
    # staff는 admin에서 로그인가능
    path("admin/", admin.site.urls),
     
    path('', HomeView.as_view(), name='home'),
    # path('blog/', include('blog.urls')),
    
    # 화면에 login 버튼 나타내는지 아닌지 정도의 역할
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # API 
    #path('drf_api/', include('drf_api.urls')),
    path('swagger/', include('swagger.urls')),
    path('crawler_api/', include('crawler_api.urls'))
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



