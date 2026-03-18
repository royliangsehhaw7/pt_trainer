from django.contrib import admin
from django.urls import path

from .views import index_view, home_view
from .views import tag_view, exercise_view

urlpatterns = [
    path('', index_view.index, name="index"),

    path('index/', index_view.index, name='index'),
    path('home/', home_view.home, name='home'),

    path('tag/', tag_view.list, name='tag_list'),
    path('tag/add/', tag_view.add, name='tag_add'),
    path("tag/edit/<int:pk>/", tag_view.edit, name="tag_edit"),
    path("tag/delete/<int:pk>/", tag_view.delete, name="tag_delete"),

    path('exercise/', exercise_view.list, name="exercise_list"),
    path('exercise/add/', exercise_view.add, name='exercise_add'),
    path("exercise/edit/<int:pk>/", exercise_view.edit, name="exercise_edit"),
    path("exercist/delete/<int:pk>/", exercise_view.delete, name="exercise_delete"),
]
