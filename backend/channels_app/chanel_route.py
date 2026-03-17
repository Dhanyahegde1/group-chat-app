from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .chanels import Channel, ChannelMember

# Create Channel API
@api_view(['POST'])
def create_channel(request):
    name = request.data.get("name")
    created_by = request.data.get("created_by")
    is_private = request.data.get("is_private", False)

    if not name or not created_by:
        return Response(
            {"error": "Channel name and creator required"},
            status=status.HTTP_400_BAD_REQUEST
        )

    channel = Channel.objects.create(
        name=name,
        created_by_id=created_by,
        is_private=is_private
    )

    # Auto-add creator as member
    ChannelMember.objects.create(
        user_id=created_by,
        channel=channel
    )

    return Response({"message": "Channel created", "channel": channel.name})

# List ALL channels (admin/discover use)
@api_view(['GET'])
def list_channels(request):
    channels = Channel.objects.all()
    data = []
    for channel in channels:
        data.append({
            "id": channel.id,
            "name": channel.name,
            "created_by": channel.created_by.username,
            "created_at": channel.created_at,
            "is_private": channel.is_private,
        })
    return Response(data)


# ── NEW: Only channels the user has joined ────────────────────────────────────
@api_view(['GET'])
def my_channels(request):
    user_id = request.query_params.get("user")
    if not user_id:
        return Response({"error": "user param required"}, status=status.HTTP_400_BAD_REQUEST)

    memberships = ChannelMember.objects.filter(user_id=user_id).select_related("channel")
    data = []
    for m in memberships:
        data.append({
            "id":         m.channel.id,
            "name":       m.channel.name,
            "created_by": m.channel.created_by.username,
            "created_at": m.channel.created_at,
            "is_private": m.channel.is_private,
        })
    return Response(data)


# ── NEW: Public channels user has NOT joined (for discovery/browse) ───────────
@api_view(['GET'])
def discover_channels(request):
    user_id = request.query_params.get("user")
    if not user_id:
        return Response({"error": "user param required"}, status=status.HTTP_400_BAD_REQUEST)

    joined_ids = ChannelMember.objects.filter(user_id=user_id).values_list("channel_id", flat=True)
    channels = Channel.objects.filter(is_private=False).exclude(id__in=joined_ids)
    data = []
    for c in channels:
        data.append({
            "id":         c.id,
            "name":       c.name,
            "created_by": c.created_by.username,
            "created_at": c.created_at,
        })
    return Response(data)


# Join Channel API
@api_view(['POST'])
def join_channel(request):
    user_id = request.data.get("user")
    channel_id = request.data.get("channel")

    if not user_id or not channel_id:
        return Response({"error": "User and Channel required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        channel = Channel.objects.get(id=channel_id)
    except Channel.DoesNotExist:
        return Response({"error": "Channel not found"}, status=status.HTTP_404_NOT_FOUND)

    if channel.is_private:
        return Response({"error": "This channel is private. Use an invite link."}, status=status.HTTP_403_FORBIDDEN)

    if ChannelMember.objects.filter(user_id=user_id, channel_id=channel_id).exists():
        return Response({"message": "User already in channel"})

    ChannelMember.objects.create(user_id=user_id, channel_id=channel_id)
    return Response({"message": "User joined channel"})


# ── NEW: Leave Channel ────────────────────────────────────────────────────────
@api_view(['DELETE'])
def leave_channel(request):
    user_id = request.data.get("user")
    channel_id = request.data.get("channel")

    if not user_id or not channel_id:
        return Response({"error": "User and Channel required"}, status=status.HTTP_400_BAD_REQUEST)

    deleted, _ = ChannelMember.objects.filter(user_id=user_id, channel_id=channel_id).delete()
    if deleted:
        return Response({"message": "Left channel"})
    return Response({"error": "You are not a member"}, status=status.HTTP_400_BAD_REQUEST)