from django.contrib import admin
from django.urls import path, include
from .views import subscription_view

from django.contrib.auth.decorators import login_required


urlpatterns = [
    # ========== backend subscriptions
    path('backend/subscription/', login_required(subscription_view.sub_list), name='subscription_list'),
    path('backend/subscription/add/', login_required(subscription_view.sub_add), name='subscription_add'),
    path('backend/subscription/edit/<int:pk>', login_required(subscription_view.sub_edit), name='subscription_edit'),
    path('backend/subscription/delete/<int:pk>', login_required(subscription_view.sub_delete), name='subscription_delete'),
]
