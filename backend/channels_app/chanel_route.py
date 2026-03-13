# Channel API Routes for defining REST APIs, including the creation of channels and joining channels

# Import API decorator for creating REST endpoints
from rest_framework.decorators import api_view

# Import Response class for sending API responses
from rest_framework.response import Response

# Import HTTP status codes
from rest_framework import status

# Import Channel and ChannelMember models
from .chanels import Channel, ChannelMember

# Import logging aspect decorator
from .aspect import log_api_call


# Create Channel API with Endpoint for post -> channels -> create
@api_view(['POST'])
@log_api_call   # Aspect decorator to log API calls
def create_channel(request):

    # Get channel name and creator ID from request
    name = request.data.get("name")
    created_by = request.data.get("created_by")

    # Validate input
    if not name or not created_by:
        return Response(
            {"error": "Channel name and creator required"},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Create channel in database
    channel = Channel.objects.create(
        name=name,
        created_by_id=created_by
    )

    # Return success response
    return Response({
        "message": "Channel created",
        "channel": channel.name
    })


# List Channels API with Endpoint for get -> channels
@api_view(['GET'])
@log_api_call   # Aspect decorator to log API calls
def list_channels(request):

    # Fetch all channels from database
    channels = Channel.objects.all()

    data = []

    # Convert queryset to JSON response format
    for channel in channels:
        data.append({
            "id": channel.id,
            "name": channel.name,
            "created_by": channel.created_by.username,
            "created_at": channel.created_at
        })

    return Response(data)


# Join Channel API with Endpoint for post -> channels -> join
@api_view(['POST'])
@log_api_call   # Aspect decorator to log API calls
def join_channel(request):

    # Get user ID and channel ID from request
    user_id = request.data.get("user")
    channel_id = request.data.get("channel")

    # Validate input
    if not user_id or not channel_id:
        return Response(
            {"error": "User and Channel required"},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Check if user already joined the channel
    if ChannelMember.objects.filter(user_id=user_id, channel_id=channel_id).exists():
        return Response({"message": "User already in channel"})

    # Create membership entry in ChannelMember table
    ChannelMember.objects.create(
        user_id=user_id,
        channel_id=channel_id
    )

    # Success response
    return Response({
        "message": "User joined channel"
    })