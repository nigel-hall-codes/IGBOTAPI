"""IGBOTSITE URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path, re_path
from API import views

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^$', views.home),
    path('testAPI/', views.testAPI.as_view()),
    path('MemesOn/', views.MemesOn.as_view()),
    path("NewDealsOn/", views.NewDealsOn.as_view()),
    path("login/", views.Login.as_view()),
    path("createuser/", views.CreateUser.as_view()),
]


