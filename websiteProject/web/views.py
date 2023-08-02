from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages


# Create your views here.


def home_page(request):
    return render(request, "web/home.html")


def register(reqest):
    return render(reqest, "web/register.html")
