from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator
from django.db import models
from websiteProject.web.validators import TextAndNumsOnlyValidator
from websiteProject.web.genres import genre_choices

UserModel = get_user_model()


# Create your models here.

class Profile(models.Model):
    username = models.CharField(
        max_length=30,
        blank=False,
        null=False,
        validators=[MinLengthValidator(2), TextAndNumsOnlyValidator],
        unique=True
    )
    email = models.EmailField(blank=False,
                              null=False,
                              unique=True)

    password = models.CharField(
        max_length=30,
        blank=False,
        null=False,
        validators=[MinLengthValidator(6), TextAndNumsOnlyValidator]
    )

    user = models.OneToOneField(
        UserModel,
        on_delete=models.CASCADE,

    )

    def __str__(self):
        return self.username


class Book(models.Model):
    title = models.CharField(max_length=255, blank=False, null=False, validators=[TextAndNumsOnlyValidator])
    author = models.CharField(max_length=30, blank=False, null=False)
    genre = models.CharField(
        max_length=255,
        choices=genre_choices,
        null=False,
        blank=False,
    )
    synopsis = models.TextField(blank=True, null=True, )
    cover_url = models.URLField(blank=False, null=False)
    book = models.TextField(blank=False, null=False)
    posted_on = models.DateTimeField(blank=True, null=True)


class Comment(models.Model):
    content = models.TextField(blank=False, null=False)
    posted_on = models.DateTimeField(blank=True, null=True)
    book_commented_on = models.ForeignKey(Book, on_delete=models.CASCADE)