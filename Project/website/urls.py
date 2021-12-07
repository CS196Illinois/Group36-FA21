from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # empty path ('') signifies the base url takes you to home
    path('search/', views.routing, name='search'),
]