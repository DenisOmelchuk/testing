from django.urls import path, re_path
from . import views

urlpatterns = [
    path('create_user/', views.api_create_user),
]