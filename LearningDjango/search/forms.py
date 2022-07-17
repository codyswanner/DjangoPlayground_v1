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
            'shelf',
            'author2_first',
            'author2_middle',
            'author2_last',
            'author3_first',
            'author3_middle',
            'author3_last',
            'is_series',
            'series'
        ]
        widgets = {
            'is_series': forms.RadioSelect
        }