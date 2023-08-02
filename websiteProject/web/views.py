from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages

from websiteProject.web.models import Profile


# Create your views here.


def home(request):
    return render(request, "web/home.html")


def register(request):
    profilee = Profile.objects.first()
    from websiteProject.web.forms import ProfileModelForm
    form = ProfileModelForm()

    if request.method == "POST":
        form = ProfileModelForm(request.POST)
        if form.is_valid():
            form.save()

    context = {
        "profile": profilee,
        "add_form": form
    }
    return render(request, "web/register.html", context)


def login(request):
    return render(request, "web/login.html")


def library(request):
    return render(request, "web/lib.html")


def book(request):
    return render(request, "web/lib_book.html")


def profile(request):
    return render(request, "web/profile.html")


def post_book(request):
    return render(request, 'web/post_book.html')


def edit_book(request):
    return render(request, 'web/edit_book')
