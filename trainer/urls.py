from django.contrib import admin
from django.urls import path

from .views import index_view, home_view
from .views import tag_view, exercise_view, workout_view,client_view

urlpatterns = [
    path('', index_view.index, name="index"),

    path('index/', index_view.index, name='index'),
    path('home/', home_view.home, name='home'),

    path('tag/', tag_view.tag_list, name='tag_list'),
    # path('tags/<str:search>/', tag_view.tag_list, name='tag_list'),    
    path('tag/add/', tag_view.tag_add, name='tag_add'),
    path("tag/edit/<int:pk>/", tag_view.tag_edit, name="tag_edit"),
    path("tag/delete/<int:pk>/", tag_view.tag_delete, name="tag_delete"),

    path('exercise/', exercise_view.list, name="exercise_list"),
    path('exercise/add/', exercise_view.add, name='exercise_add'),
    path("exercise/edit/<int:pk>/", exercise_view.edit, name="exercise_edit"),
    path("exercist/delete/<int:pk>/", exercise_view.delete, name="exercise_delete"),

    path('workout/', workout_view.workout_list, name='workout_list'),
    path('workout/add/', workout_view.workout_add, name='workout_add'),
    path('workout/<int:pk>/edit/', workout_view.workout_edit, name='workout_edit'),
    path('workout/<int:pk>/delete/', workout_view.workout_delete, name='workout_delete'),

    path('client/', client_view.client_list, name='client_list'),
    path('client/add/', client_view.client_add, name='client_add'),
    path("client/edit/<int:pk>/", client_view.client_edit, name="client_edit"),
    path("client/delete/<int:pk>/", client_view.client_delete, name="client_delete"),


    # path('workout/', workout_view.list, name="workout_list"),
    # path('workout/add/', workout_view.add, name='workout_add'),
    # path("workout/edit/<int:pk>/", workout_view.edit, name="workout_edit"),
    # path("workout/delete/<int:pk>/", workout_view.delete, name="workout_delete"),    
]
