from django import forms
from .models import Book

class NewBookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = [
            'title',
            'author_first',
            'author_middle',
            'author_last',
            'genre_1',
            'genre_2',
            'genre_3',
            'language',
            'shelf'
        ]