import os
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import logout, authenticate as auth_authenticate, get_user_model
from django.contrib.auth import login as auth_login
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from websiteProject.web.extract_text_from_docx import extract_text_from_docx
from websiteProject.web.forms import UserCreationForm, LoginForm, BookForm, CommentForm, EditCommentForm, EditBookForm, \
    StaffSuperuserCreationForm
from websiteProject.web.models import Profile, Book, Comment, Favorites, Rating

UserModel = get_user_model()


# Create your views here.


class ProfileView(View):
    @method_decorator(login_required)
    def get(self, request):
        profile = Profile.objects.get(username=request.user.username)
        books = Book.objects.all().filter(author_id=profile.id)
        favorites = Favorites.objects.all().filter(user_id_id=profile.id)
        fav_books = []

        for favorite in favorites:
            fav_books.append(Book.objects.get(id=favorite.book_id_id))

        context = {
            'books': books,
            'favs': fav_books,
            'profile_id': profile.id,
        }

        return render(request, 'web/profile.html', context)


class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, 'You are now logged out')
        return redirect('index')


class LibraryView(ListView):
    model = Book
    template_name = 'web/lib.html'
    context_object_name = 'books'

class AccessDenied(View):
    template_name = 'web/access_denied.html'

    def get(self, request):
        return render(request, self.template_name)

class IndexView(View):
    template_name = 'web/index.html'

    def get(self, request):
        return render(request, self.template_name)


def register(request):
    if request.user.is_authenticated:
        messages.error(request, 'You are already logged in')
        return redirect('index')
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
        messages.error(request, 'You are already logged in')
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


def book(request, book_pk):
    book = Book.objects.get(pk=book_pk)
    book_text = extract_text_from_docx(book.book_file)
    rating = Rating.objects.filter(book=book)
    return render(request, "web/lib_book.html", {'book_content': book_text, 'book': book})




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

            allowed_file_ext = ['docx']
            allowed_cover_ext = ['jpg', 'png']

            if book.book_file.path.split('.')[-1] not in allowed_file_ext:
                messages.error(request, "File type not allowed, please only use 'docx'")
                form = BookForm(request.POST)
                return render(request, 'web/post_book.html', {'form':form})
            if book.cover.path.split('.')[-1] not in allowed_cover_ext:
                messages.error(request, "File type not allowed, please only use 'jpg' or 'png'")
                form = BookForm(request.POST)
                return render(request, 'web/post_book.html', {'form':form})


            book.save()
            messages.success(request, 'You have posted your book successfully')
            return redirect('index')
    else:
        form = BookForm()
    return render(request, 'web/post_book.html', {'form': form})


@login_required()
def comment(request, book_pk):
    book = Book.objects.get(pk=book_pk)
    comments = Comment.objects.all().filter(book_commented_on=book_pk)
    user = User.objects.get(username=request.user.username)
    profile: Profile = Profile.objects.get(user=user)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            context = {
                'book': book,
                'comments': comments,
                'form': form,
                'profile':profile
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
            'form': form,
            'profile': profile
        }
        return render(request, 'web/comments.html', context)


@login_required()
def edit_comment(request, book_pk, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    username = request.user.username

    if comment.posted_by != Profile.objects.get(username=username) and not request.user.is_staff:
        return redirect('access_denied')

    if request.method == 'POST':
        form = EditCommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect(reverse('book_comment', args=[book_pk]))
    else:
        form = EditCommentForm(instance=comment)
    context = {
        'form': form,
        'book_pk': book_pk,
    }
    return render(request, 'web/edit_comment.html', context)

@login_required()
def delete_comment(request, book_pk, comment_pk):
    book= Book.objects.get(pk=book_pk)
    username = request.user.username
    comment = Comment.objects.get(id=comment_pk)
    if comment.posted_by != Profile.objects.get(username=username)and not request.user.is_staff:
        return redirect('access_denied')
    context= {
        'book':book,
        'comment':comment,

    }

    return render(request, 'web/delete_comment.html', context)

@login_required()
def delete_comment_confirm(request, book_pk, comment_pk):
    if request.method == 'POST':
        comment = Comment.objects.get(pk=comment_pk)
        comment.delete()
        return redirect('book_comment', book_pk= book_pk)

@login_required()
def delete_book(request, book_pk):
    book = Book.objects.get(pk=book_pk)
    author_name = book.author.username
    username = request.user.username
    if (not request.user.is_superuser) and username != author_name:
        return redirect('access_denied')
    context = {
        'book': book,
    }
    return render(request, 'web/delete_book.html', context)


@login_required()
def delete_book_confirm(request, book_pk):
    if request.method == 'POST':
        book = Book.objects.get(pk=book_pk)
        book.delete()
        os.remove(book.book_file.path)
        os.remove(book.cover.path)
        messages.success(request, 'You have successfully deleted your book')
        return redirect('profile')

    return redirect('delete_book', book_pk=book_pk)





@login_required()
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


@login_required()
def remove_favorite(request, profile_id, book_id):
    try:
        favorite = Favorites.objects.filter(user_id_id=profile_id, book_id_id=book_id)

    except ObjectDoesNotExist:
        messages.error(request, 'Does not exist')
        return redirect('index')

    profile = Profile.objects.get(id=profile_id)
    if profile.username != request.user.username:
        return redirect('access_denied')

    favorite.delete()
    messages.success(request, 'Successfully removed book from favorites')
    return  redirect('profile')

@login_required()
def edit_book(request, book_pk):
    book = Book.objects.get(pk=book_pk)
    author_name = book.author.username
    username = request.user.username
    if (not request.user.is_staff) and username != author_name:
        return redirect('access_denied')

    if request.method == 'POST':
        form = EditBookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            return redirect('library_book', book_pk=book.pk)
    else:
        form = EditBookForm(instance=book)

    context = {
        'form': form,
        'book': book,
    }
    return render(request, 'web/edit_book.html', context)

def profile_other(request, profile_pk):
    other_user = Profile.objects.get(pk=profile_pk)
    books = Book.objects.all().filter(author_id=other_user.id)
    favorites = Favorites.objects.all().filter(user_id_id=other_user.id)
    fav_books = []

    for favorite in favorites:
        fav_books.append(Book.objects.get(id=favorite.book_id_id))

    context = {
        'books': books,
        'favs': fav_books,
        'profile': other_user,
    }

    return render(request, 'web/profile_other.html', context)

@staff_member_required(login_url= 'access_denied')
def create_staff_superuser(request):
    if request.method == 'POST':
        form = StaffSuperuserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            profile = Profile.objects.create(
                user=user,
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                is_staff=True,
            )
            messages.success(request, 'You have registered a new staff member')
            return redirect('index')
    else:
        form = StaffSuperuserCreationForm()

    context = {'form': form}
    return render(request, 'web/create_staff_superuser.html', context)

@login_required()
def rate(request, book_pk ,rating):
    profile = Profile.objects.get(username=request.user.username)
    book = Book.objects.get(id=book_pk)
    Rating.objects.filter(book=book, profile=profile).delete()
    Rating.objects.create(profile=profile, rate=rating, book=book)

    return redirect('library_book', book_pk= book_pk)


