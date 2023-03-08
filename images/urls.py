"""images URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from accounts.views import AccountTierViewSet, ImageViewSet, UserImageViewSet

router = DefaultRouter()
router.register(r'account_tiers', AccountTierViewSet, basename='account-tier')
router.register(r'images', ImageViewSet, basename='image')
router.register(r'user_images', UserImageViewSet, basename='user-image')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
]
