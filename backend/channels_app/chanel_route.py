from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .chanels import Channel, ChannelMember

# Create Channel API 
@api_view(['POST'])
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

# List Channels API 
@api_view(['GET'])
def list_channels(request):

    # Fetch all channels
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



# Join Channel API 
@api_view(['POST'])
def join_channel(request):

    # Get user and channel from request
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

    # Create membership entry
    ChannelMember.objects.create(
        user_id=user_id,
        channel_id=channel_id
    )

    # Success response
    return Response({
        "message": "User joined channel"
    })
