import os
from django.contrib.auth import logout, authenticate as auth_authenticate, get_user_model
from django.contrib.auth import login as auth_login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from websiteProject.web.extract_text_from_docx import extract_text_from_docx
from websiteProject.web.forms import UserCreationForm, LoginForm, BookForm, CommentForm
from websiteProject.web.models import Profile, Book, Comment, Favorites

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


class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, 'You are now logged out')
        return redirect('index')


class LibraryView(ListView):
    model = Book
    template_name = 'web/lib.html'
    context_object_name = 'books'


def book(request, book_pk):
    book = Book.objects.get(pk=book_pk)
    book_text = extract_text_from_docx(book.book_file)
    return render(request, "web/lib_book.html", {'book_content': book_text, 'book': book})


class ProfileView(View):
    @method_decorator(login_required)
    def get(self, request):
        author = Profile.objects.get(username=request.user.username)
        books = Book.objects.all().filter(author_id=author.id)
        favorites = Favorites.objects.all().filter(user_id_id=author.id)
        fav_books = []
        for favorite in favorites:
            fav_books.append(Book.objects.get(id=favorite.book_id_id))

        context = {
            'books': books,
            'favs': fav_books,
        }

        return render(request, 'web/profile.html', context)


@login_required()
def post_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            user = User.objects.get(username=request.user.username)
            profile: Profile = Profile.objects.get(user=user)

            book = form.save(commit=False)
            book.author = profile
            book.posted_on = timezone.now()
            book.save()

            return redirect('index')
    else:
        form = BookForm()
    return render(request, 'web/post_book.html', {'form': form})


@login_required()
def comment(request, book_pk):
    book = Book.objects.get(pk=book_pk)
    comments = Comment.objects.all().filter(book_commented_on=book_pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            user = User.objects.get(username=request.user.username)
            profile: Profile = Profile.objects.get(user=user)

            context = {
                'book': book,
                'comments': comments,
                'form': form
            }
            comment = form.save(commit=False)
            comment.book_commented_on = book
            comment.posted_by = profile
            comment.posted_on = timezone.now()
            comment.save()

            return redirect(reverse('book_comment', args=[book_pk]))
    else:
        form = CommentForm()
        context = {
            'book': book,
            'comments': comments,
            'form': form
        }
        return render(request, 'web/comments.html', context)

@login_required()
def edit_book(request):  # todo class based view
    return render(request, 'web/edit_book.html')

@login_required()
def delete_book(request, book_pk):
    username = request.user.username
    book = Book.objects.get(pk=book_pk)
    author_name = book.author.username
    if (not request.user.is_staff) and username != author_name:
        return redirect('access_denied')
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


class AccessDenied(View):
    template_name = 'web/access_denied.html'

    def get(self, request):
        return render(request, self.template_name)


def favorite(request, book_pk):
    book = Book.objects.get(pk=book_pk)
    user = request.user
    profile = Profile.objects.get(user=user)

    if Favorites.objects.filter(user_id_id=profile.id, book_id_id=book.id):
        messages.error(request, 'You have already favorited this book')
        return redirect('library_book', book_pk=book_pk)

    favorite_instance = Favorites(
        user_id_id=profile.id,
        book_id_id=book.id,
        favorited_on=timezone.now(),
    )

    favorite_instance.save()

    messages.success(request, 'You have favorited this book')
    return redirect('library_book', book_pk=book_pk)