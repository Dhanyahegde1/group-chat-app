from django.urls import path
from .chanel_route import create_channel


urlpatterns = [
    path('create/', create_channel),
]