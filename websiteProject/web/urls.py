from django.contrib import admin
from django.urls import path
from websiteProject.web import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('register', views.register, name='register'),
    path('login', views.login_view, name='login'),
    path('library', views.LibraryView.as_view(), name='library'),
    path('library/book/<int:book_pk>', views.book, name='library_book'),
    path('profile', views.ProfileView.as_view(), name='profile'),
    path('profile/post', views.post_book, name="post_book"),
    path('library/book/<int:book_pk>/edit', views.edit_book, name='edit_book'),
    path('library/book/<int:book_pk>/comment', views.comment, name='book_comment'),
    path('logout', views.LogoutView.as_view(), name='logout'),
    path('delete/<int:book_pk>/', views.delete_book, name='delete_book'),
    path('delete_confirm/<int:book_pk>/', views.delete_book_confirm, name='delete_book_confirm'),
    path('access_denied', views.AccessDenied.as_view(), name='access_denied'),
    path('library/book/<int:book_pk>/favorite', views.favorite, name='favorite'),
    path('profile/remove_favorite/<int:profile_id>/<int:book_id>', views.remove_favorite, name='remove_favorite'),

]