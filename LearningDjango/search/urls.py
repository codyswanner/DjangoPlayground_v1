from django.urls import path
from . import views

app_name = 'search'
urlpatterns = [
    path('', views.index, name="index"),
    path('advanced_search', views.advanced_search, name='advanced_search'),
    path('results', views.search_results, name='search_results'),
    path('new_book_form', views.new_book_form, name='new_book_form'),
    # path('new_book_confirmation', views.new_book_confirmation, name='new_book_confirmation')
]
