from django.core.validators import MinLengthValidator
from django.db import models
from websiteProject.web.validators import TextAndNumsOnlyValidator
from websiteProject.web.genres import genre_choices


# Create your models here.

class Profile(models.Model):
    username = models.CharField(
        max_length=30,
        blank=False,
        null=False,
        validators=[MinLengthValidator(2), TextAndNumsOnlyValidator]
    )
    email = models.EmailField(blank=False,
                              null=False, )

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
    synopsis = models.TextField(blank=True, null=True,)
    cover_url = models.URLField(blank=False, null=False)
