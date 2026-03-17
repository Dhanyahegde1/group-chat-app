from django.urls import path
from .chanel_route import create_channel, list_channels, join_channel, my_channels, discover_channels, leave_channel
from .aspect import generate_invite, request_join, respond_invite, check_invite_status, get_pending_invite

urlpatterns = [
    path('create/', create_channel),
    path('', list_channels),
    path('join/', join_channel),
    path('my/', my_channels),
    path('discover/', discover_channels),
    path('leave/', leave_channel),
    path('invite/generate/', generate_invite),
    path('invite/join/<str:code>/', request_join),
    path('invite/respond/', respond_invite),
    path('invite/status/<str:code>/', check_invite_status),
    path('invite/pending/<int:channel_id>/', get_pending_invite),
]