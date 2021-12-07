from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # empty path ('') signifies the base url takes you to home
    path('search-symptoms/', views.search, name='search-symptoms'),
    path('search-diseases/', views.search_disease, name='search-diseases')
]