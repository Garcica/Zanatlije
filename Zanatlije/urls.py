"""Zanatlije URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from ZanatlijeApp import views

urlpatterns = [
    path('', views.search, name="search"),
    path('odobravanje/', views.admin_odobravanje, name="adminOdobravanje"),
    path('adminPanel/', views.admin, name="adminPanel"),
    path('admin/', admin.site.urls),
    path('login/', views.login_req, name='login'),
    path('register/', views.reister_req, name='register'),
    path('profile/', views.profile, name='myprofile'),
    path('edit/', views.edit, name='edit')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
