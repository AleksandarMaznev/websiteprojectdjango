from django.db import models
from .genres import genre_choices as genre_choices


# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=255, blank=False, null=False)
    author = models.CharField(max_length=255, blank=False, null=False)
    genre = models.CharField(
        max_length=255,
        choices=genre_choices,
        null=False,
        blank=False,
    )
