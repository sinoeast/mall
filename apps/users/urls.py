"""mall URL Configuration

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
from django.contrib import admin
from django.urls import path, include

from apps.users.views import Register, UsernameCountView, MobileCountView, LoginView, LogoutView, UserCenterInfoView

urlpatterns = [
    path('register/', Register.as_view(), name='register'),
    path('register/<str:username>', UsernameCountView.as_view(), name='UsernameCountView'),
    path('register', MobileCountView.as_view(), name='mobileCountView'),
    path('login',LoginView.as_view(),name='login'),
    path('logout',LogoutView.as_view(),name='logout'),
    path('center',UserCenterInfoView.as_view(),name='center'),
]
