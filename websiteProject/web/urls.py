from django.contrib import admin
from django.urls import path
from websiteProject.web import views

urlpatterns = [
    path('register', views.register, name='register'),
    path('custom', views.custom, name='custom'),
    path('home', views.home, name='home'),
    ]