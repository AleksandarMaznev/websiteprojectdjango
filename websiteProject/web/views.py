from django.contrib.auth import logout, authenticate as auth_authenticate, get_user_model
from django.contrib.auth import login as auth_login
from django.forms import forms
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from websiteProject.web.forms import ProfileModelForm, LoginForm
from websiteProject.web.models import Profile

UserModel = get_user_model()


# Create your views here.


def index(request):
    profile = request.user
    context = {
        "profile": profile
    }
    return render(request, "web/index.html", context)


# TODO fix registering using superuser nicks traceback error
def register(request):
    profilee = Profile.objects.first()
    form = ProfileModelForm()

    if request.method == "POST":
        form = ProfileModelForm(request.POST)
        if form.is_valid():
            user = UserModel.objects.create_user(
                username=form.cleaned_data.get('username'),
                email=form.cleaned_data.get('email'),
                password=form.cleaned_data.get('password')
            )
            form.instance.user = user
            form.save()

            auth_login(request, user)
            return redirect('index')

    context = {
        "profile": profilee,
        "add_form": form,
        "errors": form.errors,
    }
    return render(request, "web/register.html", context)


def login_view(request):
    if request.user.is_authenticated:
        return redirect('index')

    form = LoginForm()

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            print('valid')
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = auth_authenticate(username=username, password=password)

            if user is not None:
                auth_login(request, user)
                return redirect('index')
            else:
                form.add_error("username", "Incorrect username or password")
        else:
            for field in form:
                print("Field Error:", field.name, field.errors)

    context = {
        "add_form": form,
    }

    return render(request, "web/login.html", context)


def logout_view(request):
    logout(request)
    messages.success(request, 'You are now logged out')
    return redirect('index')


def library(request):
    return render(request, "web/lib.html")


def book(request):
    return render(request, "web/lib_book.html")


def profile(request):
    return render(request, "web/profile.html")


def post_book(request):
    return render(request, 'web/post_book.html')


def edit_book(request):
    return render(request, 'web/edit_book.html')
