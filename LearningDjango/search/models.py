from django.db import models

# Create your models here.


class Stuff(models.Model):
    name = models.CharField(max_length=20)
    color = models.CharField(max_length=20)


def __str__(self):
    return self.name


class Books(models.Model):
    title = models.CharField(max_length=50, null=False)
    author_first = models.CharField(max_length=30, null=False)
    author_middle = models.CharField(max_length=30, null=True)
    author_last = models.CharField(max_length=30, null=False)
    genre_1 = models.CharField(max_length=30, null=False)
    genre_2 = models.CharField(max_length=30, null=True)
    genre_3 = models.CharField(max_length=30, null=True)
    language = models.CharField(max_length=20)
    shelf = models.CharField(max_length=10, null=False)

