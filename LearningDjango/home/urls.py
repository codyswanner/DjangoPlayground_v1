from django.urls import path
from . import views

app_name = 'home'
urlpatterns = [
    path('', views.index, name="index"),
    path('search_redirect/', views.search_redirect, name='search_redirect'),
]