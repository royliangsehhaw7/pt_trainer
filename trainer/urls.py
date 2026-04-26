from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

from .views import account_view, index_view, home_view
from .views import index_view, tag_view, exercise_view, workout_view, client_view, account_view, appointment_view, ai_view

from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('', index_view.index, name="index"),

    path('index/', index_view.index, name='index'),
    path('home/', login_required(home_view.home), name='home'),


    # ============================== social auth django ======================================= #
    # social-auth-django provides the 'social:begin' namespace
    path('social-auth/', include('social_django.urls', namespace='social')),
    path("social-login/", account_view.social_login, name="social_login"),


    # =============================  django authentication ==================================== #
    path("login/", account_view.login_page, name="login"),
    path("register/", account_view.register_page, name="register"),
    path("", include("django.contrib.auth.urls")),


    # =============================  trainer app processes ==================================== #
    path('client/', login_required(client_view.client_list), name="client_list"),
    path('client/add/', login_required(client_view.client_add), name='client_add'),
    path("client/edit/<int:pk>/", login_required(client_view.client_edit), name="client_edit"),
    path("client/delete/<int:pk>/", login_required(client_view.client_delete), name="client_delete"),

    path('tag/', login_required(tag_view.tag_list), name='tag_list'),
    # path('tags/<str:search>/', tag_view.tag_list, name='tag_list'),    
    path('tag/add/', login_required(tag_view.tag_add), name='tag_add'),
    path("tag/edit/<int:pk>/", login_required(tag_view.tag_edit), name="tag_edit"),
    path("tag/delete/<int:pk>/", login_required(tag_view.tag_delete), name="tag_delete"),
    path("tags/", tag_view.get_tags, name="get_tags"),

    path('exercise/', login_required(exercise_view.exercise_list), name="exercise_list"),
    path('exercise/add/', login_required(exercise_view.exercise_add), name='exercise_add'),
    path("exercise/edit/<int:pk>/", login_required(exercise_view.exercise_edit), name="exercise_edit"),
    path("exercise/delete/<int:pk>/", login_required(exercise_view.exercise_delete), name="exercise_delete"),
    path('exercises/tags/', exercise_view.get_exercises_by_tags, name="exercise_by_tags"),
    
    path('client/', login_required(client_view.client_list), name='client_list'),
    path('client/add/', login_required(client_view.client_add), name='client_add'),
    path("client/edit/<int:pk>/", login_required(client_view.client_edit), name="client_edit"),
    path("client/delete/<int:pk>/", login_required(client_view.client_delete), name="client_delete"),
    # json
    path('client/info/', client_view.get_client_info, name='get_client_info'),

    #
    # NOTE:
    # path('client/info/<int:pk>', client_view.get_client_info, name='get_client_info') => client/info/1
    # def get_client_info(request, pk)
    #
    # path('client/info/', client_view.get_client_info, name='get_client_info')
    # def get_client_info(request)
    # pk = request.GET.get('pk')
    #

    path('workout/', workout_view.workout_list, name='workout_list'),
    path('workout/add/', workout_view.workout_add, name='workout_add'),
    path('workout/edit/<int:pk>/', workout_view.workout_edit, name='workout_edit'),
    path('workout/delete/<int:pk>/', workout_view.workout_delete, name='workout_delete'),

    path('appointment/', appointment_view.appoint_list, name='appointment_list'),
    path('appointment/calender/', appointment_view.appoint_calendar, name='appointment_calendar'),
    path('appointment/add/', appointment_view.appoint_add, name='appointment_add'),
    path('appointment/edit/<int:pk>/', appointment_view.appoint_edit, name='appointment_edit'),
    path('appointment/delete/<int:pk>/', appointment_view.appoint_delete, name='appointment_delete'),


    # path('calendar/', appointment_view.calendar_view, name='calendar'),
    path('calendar_json/', appointment_view.calendar_json_view, name='calendar_json'),

    # 
    # path('', include('social_django.urls', namespace='social')),


    path('ai/generate/<str:prompt>', ai_view.generate, name='ai_gen'),
    path('ai/workout/unstructured/', ai_view.generate_workout_unstructured, name='ai_workout_unstructured'),
    path('ai/workout/client/<int:client_id>/exercises/<int:exe_count>', ai_view.generate_workout_structured, name='ai_workout_structured'),
]
