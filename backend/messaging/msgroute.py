# Import Django path function for URL routing
from django.urls import path

# Import messaging API views
from .msgservice import send_message, get_messages


# ---------------------------------------------------
# Messaging API Routes
# ---------------------------------------------------
# These endpoints handle sending messages
# and retrieving messages from a specific channel
urlpatterns = [

    # Endpoint: POST /messages/send/
    # Sends a new message to a channel
    path('send/', send_message),

    # Endpoint: GET /messages/channel/<channel_id>/
    # Returns all messages for the specified channel
    path('channel/<int:channel_id>/', get_messages),
]
