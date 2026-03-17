from django.urls import path
from .views import register, login, list_users

urlpatterns = [
    path('register/', register),
    path('login/', login),
    path('list/', list_users),
]