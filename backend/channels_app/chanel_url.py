from django.urls import path
from .chanel_route import create_channel, list_channels, join_channel

# Channel API Routes
urlpatterns = [

    # Creates a new chat channel
    path('create/', create_channel),

    # Returns a list of all channels
    path('', list_channels),

    # Allows a user to join an existing channel
    path('join/', join_channel),
]

