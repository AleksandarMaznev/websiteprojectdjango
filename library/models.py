from django.db import models


# Create your models here.
class Book(models.Model):

    genre_choices = [
        ("FAN", "Fantasy"),
        ("SCIF", "Sci-Fi"),
        ("NFAN", "Nonfiction"),
        ("SR", "Senior"),
        ("GR", "Graduate"),
]

    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    genre = mod