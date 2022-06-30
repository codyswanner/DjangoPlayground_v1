from django.urls import path
from . import views

app_name = 'search'
urlpatterns = [
    path('', views.index, name="index"),
    path('advanced_search', views.advanced_search, name='advanced_search'),
    path('results', views.search_results, name='search_results')
]
