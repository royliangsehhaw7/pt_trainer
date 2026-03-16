from django.contrib import admin
from django.urls import path

from .views import index_view, home_view

urlpatterns = [
    path('', index_view.index, name="index"),

    path('index/', index_view.index, name='index'),
    path('home/', home_view.home, name='home')
]
