import os

from django.contrib.auth import logout, authenticate as auth_authenticate, get_user_model
from django.contrib.auth import login as auth_login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from django.views import View
from django.contrib.auth.decorators import login_required

from websiteProject.web.extract_text_from_docx import extract_text_from_docx
from websiteProject.web.forms import UserCreationForm, LoginForm, BookForm
from websiteProject.web.models import Profile, Book

UserModel = get_user_model()


# Create your views here.


class IndexView(View):
    template_name = 'web/index.html'

    def get(self, request):
        return render(request, self.template_name)


def register(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()

            profile = Profile.objects.create(
                user=user,
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email']
            )
            auth_user = auth_authenticate(username=user.username, password=form.cleaned_data['password1'])
            if auth_user:
                auth_login(request, auth_user)
                return redirect('index')

    context = {
        "add_form": form,
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


# def logout_view(request):
#     logout(request)
#     messages.success(request, 'You are now logged out')
#     return redirect('index')

class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, 'You are now logged out')
        return redirect('index')


def library(request):
    books = Book.objects.all()
    context = {'books': books}
    return render(request, "web/lib.html", context)


def book(request, book_pk):
    book = Book.objects.get(pk=book_pk)
    book_text = extract_text_from_docx(book.book_file)
    return render(request, "web/lib_book.html", {'book_content': book_text, 'book': book})


class ProfileView(View):
    def get(self, request):
        context = {}
        author = Profile.objects.get(username=request.user.username)
        books = Book.objects.all().filter(author_id=author.id)
        context = {'books': books}
        print('books')

        return render(request, 'web/profile.html', context)


@login_required
def post_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            user = User.objects.get(username=request.user.username)  # Replace 'username' with the actual username
            profile: Profile = Profile.objects.get(user=user)

            book = form.save(commit=False)
            book.author = profile
            book.posted_on = timezone.now()
            book.save()

            return redirect('index')  # Redirect to success page
    else:
        form = BookForm()
    return render(request, 'web/post_book.html', {'form': form})


def edit_book(request):  # todo class based view
    return render(request, 'web/edit_book.html')


def delete_book(request, book_pk):
    book = Book.objects.get(pk=book_pk)
    context = {
        'book': book,
    }
    return render(request, 'web/delete_book.html', context)


def delete_book_confirm(request, book_pk):
    if request.method == 'POST':
        book = Book.objects.get(pk=book_pk)
        book.delete()
        os.remove(book.book_file.path)
        os.remove(book.cover.path)
        return redirect('profile')

    return redirect('delete_book', book_pk=book_pk)
