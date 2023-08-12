from django.contrib import admin
from websiteProject.web.models import Profile, Book, Comment, Favorites, CustomUserManager
# Register your models here.

admin.site.register(Profile)
admin.site.register(Book)
admin.site.register(Comment)
admin.site.register(Favorites)
