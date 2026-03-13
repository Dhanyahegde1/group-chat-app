from django.urls import path
from .chanel_route import create_channel, list_channels, join_channel
from .aspect import generate_invite, request_join, respond_invite, check_invite_status, get_pending_invite

# Channel API Routes
urlpatterns = [

    # Creates a new chat channel
    path('create/', create_channel),

    # Returns a list of all channels
    path('', list_channels),

    # Allows a user to join an existing channel
    path('join/', join_channel),
     path('invite/generate/', generate_invite),        
    path('invite/join/<str:code>/', request_join),    
    path('invite/respond/', respond_invite),
    path('invite/status/<str:code>/', check_invite_status),
    path('invite/pending/<int:channel_id>/', get_pending_invite),
]

