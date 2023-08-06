from django.contrib.auth import logout, authenticate, get_user_model
from django.contrib.auth import login as auth_login
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages

from websiteProject.web.models import Profile

UserModel = get_user_model()


# Create your views here.


def index(request):
    profile = request.user
    context = {
        "profile": profile
    }
    return render(request, "web/index.html", context)


def register(request):
    profilee = Profile.objects.first()
    from websiteProject.web.forms import ProfileModelForm
    form = ProfileModelForm()

    # 'AnonymousUser' object has no attribute '_meta' fix
    if request.user.is_authenticated:
        user = request.user
    else:
        return redirect('index')
    #  ----------------------------------------------------

    if request.method == "POST":
        form = ProfileModelForm(request.POST)
        if form.is_valid():
            user = UserModel.objects.create_user(
                username=form.cleaned_data.get('username'),
                email=form.cleaned_data.get('email'),
                password=form.cleaned_data.get('password1')
            )
            form.instance.user = user
            form.save()

            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            auth_login(request, user)
            return redirect('index')

    context = {
        "profile": profilee,
        "add_form": form,
        "errors": form.errors,
    }
    return render(request, "web/register.html", context)


def login(request):
    if request.user.is_authenticated:
        return redirect('index')

    form = LoginForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            form.add_error("username", "Incorrect username or password")

    context = {
        "form": form,
    }
    return render(request, "web/login.html", context)


def logout_view(request):
    logout(request)
    # Redirect to a success page.


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
