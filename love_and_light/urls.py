"""
URL configuration for love_and_light project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny
from love_and_lightapp.views import home



schema_view = get_schema_view(
    openapi.Info(
        title="Property API",
        default_version='v1',
        description="API documentation for Property management system",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="support@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    path('', include('love_and_lightapp.urls')),
    path('accounts/', include('allauth.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]

if settings.DEBUG:  # This ensures it's only applied in development
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
