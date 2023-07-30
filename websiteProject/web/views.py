from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages


# Create your views here.


def register(request):
    if request.method == 'POST':
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']

        user = User.objects.create_user(username=username, password=password, email=email)
        user.save()
        print('user created')
        return redirect('/custom')

    return render(request, 'web/register.html')


def custom(request):
    return render(request, 'web/custom.html')


def home(request):
    return render(request, 'web/home.html')
