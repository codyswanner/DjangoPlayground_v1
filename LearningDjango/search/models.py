from django.db import models

# Create your models here.

#
# class Stuff(models.Model):
#     name = models.CharField(max_length=20)
#     color = models.CharField(max_length=20)
#
#
# def __str__(self):
#     return self.name


class Book(models.Model):
    title = models.CharField(max_length=50, null=False, blank=False)
    author_first = models.CharField(max_length=30, null=False, blank=False)
    author_middle = models.CharField(max_length=30, null=True, blank=True)
    author_last = models.CharField(max_length=30, null=False, blank=False)
    genre_1 = models.CharField(max_length=30, null=False, blank=False)
    genre_2 = models.CharField(max_length=30, null=True, blank=True)
    genre_3 = models.CharField(max_length=30, null=True, blank=True)
    language = models.CharField(max_length=20, null=False, blank=False)
    shelf = models.CharField(max_length=10, null=False, blank=False)

    def __str__(self):
        return self.title
