from django.contrib import admin
from django.urls import path
from websiteProject.web import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register', views.register, name='register'),
    path('')
    ]