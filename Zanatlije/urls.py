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
    path('', views.login_req, name='home'),
    path('/', views.login_req, name='home'),
    path('odobravanje/', views.admin_odobravanje, name="adminOdobravanje"),
    path('adminPanel/', views.admin, name="adminPanel"),
    path('admin/', admin.site.urls),
    path('login/', views.login_req, name='login'),
    path('register/', views.register_req, name='register'),
    path('myprofile/<korisnik>/', views.profile, name='myprofile'),
    path('edit/', views.edit, name='edit'),
    path('profile/<neki_profil>/', views.someones_profile, name='someones_profile'),
    path('logout/', views.logout_req, name='logout'),
    path('self_delete/', views.self_delete_req, name='self_delete_req'),
    path('moderatorPanel/', views.moderator, name='moderatorPanel'),
    path('search/', views.search, name='search'),
    path('caskanja/<username>', views.caskanjeDetalj, name='caskanjeDetalj'),
    path('poruka/', views.postPoruku, name='postPoruku'),
    path('poruke/', views.poruke, name='poruke'),
    path('chats/', views.chats, name='chats'),
    path('oceni/', views.oceni, name='oceni'),
    path('komentarisi/', views.komentarisi, name='komentarisi')
    #path('saradnja', views.saradnja, name='saradnja')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
