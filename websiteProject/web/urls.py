from django.contrib import admin
from django.urls import path
from websiteProject.web import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register', views.register, name='register'),
    path('login', views.login_view, name='login'),
    path('library', views.library, name='library'),
    path('library/book/<int:id>', views.book, name='library_book'),
    path('profile', views.profile, name='profile'),
    path('profile/post', views.post_book, name="post_book"),
    path('library/book/<int:id>/edit', views.edit_book, name='edit_book'),
    path('logout', views.logout_view, name='logout')
    ]