from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from .views import account_view, index_view, home_view
from .views import index_view, tag_view, exercise_view, workout_view, client_view, account_view

from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', index_view.index, name="index"),

    path('index/', index_view.index, name='index'),
    path('home/', login_required(home_view.home), name='home'),

    # path('login/', account_view.login_page, name='login'),
    # path('register/', account_view.register_page, name='register'),
    # path('logout/', account_view.account_logout, name="logout"),
    # 1. PLACE CUSTOM OVERRIDES FIRST
    # path('accounts/password_reset/', auth_views.PasswordResetView.as_view(
    #     template_name='trainer/registration/password_reset_form.html'
    # ), name='password_reset'),
    # 2. THEN INCLUDE THE REST OF THE AUTH URLS
    path("accounts/", include("django.contrib.auth.urls")),
    path("accounts/register/", account_view.register_page, name="register"),

    path('client/', login_required(client_view.client_list), name="client_list"),
    path('client/add/', login_required(client_view.client_add), name='client_add'),
    path("client/edit/<int:pk>/", login_required(client_view.client_edit), name="client_edit"),
    path("client/delete/<int:pk>/", login_required(client_view.client_delete), name="client_delete"),

    
    path('tag/', login_required(tag_view.tag_list), name='tag_list'),
    # path('tags/<str:search>/', tag_view.tag_list, name='tag_list'),    
    path('tag/add/', login_required(tag_view.tag_add), name='tag_add'),
    path("tag/edit/<int:pk>/", login_required(tag_view.tag_edit), name="tag_edit"),
    path("tag/delete/<int:pk>/", login_required(tag_view.tag_delete), name="tag_delete"),
    # json
    path("tags/", tag_view.get_tags, name='get_tags'),

    
    path('exercise/', login_required(exercise_view.exercise_list), name="exercise_list"),
    path('exercise/add/', login_required(exercise_view.exercise_add), name='exercise_add'),
    path("exercise/edit/<int:pk>/", login_required(exercise_view.exercise_edit), name="exercise_edit"),
    path("exercise/delete/<int:pk>/", login_required(exercise_view.exercise_delete), name="exercise_delete"),
    # json
    path("exercises/tags/", exercise_view.get_exercises_params, name='get_exerises_by_tags'),


    path('workout/', workout_view.workout_list, name='workout_list'),
    path('workout/add/', workout_view.workout_add, name='workout_add'),
    path('workout/<int:pk>/edit/', workout_view.workout_edit, name='workout_edit'),
    path('workout/<int:pk>/delete/', workout_view.workout_delete, name='workout_delete'),


    path('client/', login_required(client_view.client_list), name='client_list'),
    path('client/add/', login_required(client_view.client_add), name='client_add'),
    path("client/edit/<int:pk>/", login_required(client_view.client_edit), name="client_edit"),
    path("client/delete/<int:pk>/", login_required(client_view.client_delete), name="client_delete"),
    path('client/id/<int:pk>', login_required(client_view.get_client_by_id), name="get_client_by_id")


    # path('workout/', workout_view.list, name="workout_list"),
    # path('workout/add/', workout_view.add, name='workout_add'),
    # path("workout/edit/<int:pk>/", workout_view.edit, name="workout_edit"),
    # path("workout/delete/<int:pk>/", workout_view.delete, name="workout_delete"),    
]
