from django.contrib import admin
from websiteProject.web.models import Profile, Book, Comment, Favorites, CustomUserManager


# Register your models here.

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'genre', 'posted_on')
    list_filter = ('author', 'genre', 'posted_on')
    ordering = ('-posted_on',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('content', 'posted_by', 'book_commented_on', 'posted_on')
    list_filter = ('posted_by', 'book_commented_on', 'posted_on')
    ordering = ('-posted_on',)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_active', 'is_staff')
    list_filter = ('is_active', 'is_staff')
    search_fields = ('username', 'email')
    ordering = ('username',)


@admin.register(Favorites)
class FavoritesAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'book_id', 'favorited_on')
    list_filter = ('user_id', 'book_id', 'favorited_on')
    search_fields = ('user_id__username', 'book_id__title')
    ordering = ('-favorited_on',)
