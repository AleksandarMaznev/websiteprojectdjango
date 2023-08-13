from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator
from django.db import models
from django.db.models import Avg

from websiteProject.web.custom_upload_files import upload_file
from websiteProject.web.validators import TextAndNumsOnlyValidator
from websiteProject.web.genres import genre_choices
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

UserModel = get_user_model()


# Create your models here.


class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, email, password, **extra_fields)


class Profile(AbstractBaseUser):
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

    user = models.OneToOneField(
        UserModel,
        on_delete=models.CASCADE,
        related_name='profile',
    )

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username


class Book(models.Model):
    title = models.CharField(max_length=255, blank=False, null=False, validators=[TextAndNumsOnlyValidator])
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    genre = models.CharField(
        max_length=255,
        choices=genre_choices,
        null=False,
        blank=False,
    )
    synopsis = models.TextField(blank=True, null=True, )
    cover = models.FileField(upload_to=upload_file)
    book_file = models.FileField(upload_to=upload_file)
    posted_on = models.DateTimeField(blank=True, null=True)

    def average_rating(self) -> float:
        return Rating.objects.filter(book=self).aggregate(avg=Avg("rate"))["avg"] or 0


class Comment(models.Model):
    posted_by = models.ForeignKey(Profile, on_delete=models.CASCADE)
    content = models.TextField(blank=False, null=False)
    posted_on = models.DateTimeField(blank=True, null=True)
    book_commented_on = models.ForeignKey(Book, on_delete=models.CASCADE)


class Favorites(models.Model):
    user_id = models.ForeignKey(Profile, on_delete=models.CASCADE)
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE)
    favorited_on = models.DateTimeField(blank=True, null=True)


class Rating(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    rate = models.IntegerField(default=0)

