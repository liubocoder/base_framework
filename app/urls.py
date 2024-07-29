"""
URL configuration for base_framework project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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

from django.conf import settings
from django.urls import path, include
from drf_spectacular.views import SpectacularJSONAPIView, SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

from .api.urls import urlpatterns as api_urls

urlpatterns = [
    path("webapi/v1/", include(api_urls)),
]

if settings.DEBUG:
    urlpatterns.append(path('swagger/json/', SpectacularJSONAPIView.as_view(), name='schema'))
    urlpatterns.append(path('swagger/ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'))
    urlpatterns.append(path('swagger/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'))