# Import Django path function for URL routing
from django.urls import path

# Import channel API views
from .chanel_route import create_channel, list_channels, join_channel


# ---------------------------------------------------
# Channel API Routes are the endpoints foor handeling
# ---------------------------------------------------
# These endpoints handle channel creation,
# listing available channels, and joining channels
urlpatterns = [

    # Endpoint: POST /channels/create/
    # Creates a new chat channel
    path('create/', create_channel),

    # Endpoint: GET /channels/
    # Returns a list of all channels
    path('', list_channels),

    # Endpoint: POST /channels/join/
    # Allows a user to join an existing channel
    path('join/', join_channel),
]

