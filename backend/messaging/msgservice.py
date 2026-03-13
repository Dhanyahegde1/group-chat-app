# Import API decorator for creating REST endpoints
from rest_framework.decorators import api_view

# Import Response class for sending API responses
from rest_framework.response import Response

# Import HTTP status codes
from rest_framework import status

# Import Message model
from .models import Message

# Import Channel and User models
from channels_app.chanels import Channel
from users.models import User


# ---------------------------------------------------
# Send Message API
# Endpoint: POST /messages/send
# ---------------------------------------------------
@api_view(['POST'])
def send_message(request):

    # Get data from request body
    user_id = request.data.get("user")
    channel_id = request.data.get("channel")
    content = request.data.get("content")

    # Validate input fields
    if not user_id or not channel_id or not content:
        return Response(
            {"error": "User, channel and message required"},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Create message in database
    message = Message.objects.create(
        sender_id=user_id,
        channel_id=channel_id,
        content=content
    )

    # Return success response
    return Response({
        "message": "Message sent",
        "content": message.content
    })


# ---------------------------------------------------
# Get Messages API
# Endpoint: GET /messages/<channel_id>
# ---------------------------------------------------
@api_view(['GET'])
def get_messages(request, channel_id):

    # Fetch all messages belonging to a channel
    messages = Message.objects.filter(channel_id=channel_id)

    data = []

    # Convert queryset to response format
    for msg in messages:
        data.append({
            "user": msg.sender.username,
            "message": msg.content,
            "time": msg.created_at
        })

    return Response(data)

