from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .chanels import Channel, ChannelMember
from users.models import User
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
    username = request.query_params.get('username')
    try:
        user = User.objects.get(username=username)
        # Channels created by user
        created = Channel.objects.filter(created_by=user)
        # Channels user has joined
        joined_ids = ChannelMember.objects.filter(user=user).values_list('channel_id', flat=True)
        joined = Channel.objects.filter(id__in=joined_ids)
        # Combine both
        channels = (created | joined).distinct()
        data = [{"id": c.id, "name": c.name} for c in channels]
        return Response(data)
    except User.DoesNotExist:
        return Response([])

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
