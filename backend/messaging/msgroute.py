from django.urls import path
from messaging.msgservice import send_message, get_dm_history_api

urlpatterns = [
    path('send/', send_message),
    path('dm/<str:my_username>/<str:other_username>/', get_dm_history_api),
]