from django.db import models

# Create your models here.


class Stuff(models.Model):
    name = models.CharField(max_length=20)
    color = models.CharField(max_length=20)


def __str__(self):
    return self.name


class Books(models.Model):
    title = models.CharField(max_length=50)
    author = models.CharField(max_length=50)
    genre_1 = models.CharField(max_length=30)
    genre_2 = models.CharField(max_length=30)
    genre_3 = models.CharField(max_length=30)
    shelf = models.CharField(max_length=10)

