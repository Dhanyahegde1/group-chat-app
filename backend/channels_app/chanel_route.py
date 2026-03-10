from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .chanels import Channel


@api_view(['POST'])
def create_channel(request):

    name = request.data.get("name")
    created_by = request.data.get("created_by")

    if not name or not created_by:
        return Response(
            {"error": "Channel name and creator required"},
            status=status.HTTP_400_BAD_REQUEST
        )

    channel = Channel.objects.create(
        name=name,
        created_by_id=created_by
    )

    return Response({
        "message": "Channel created",
        "channel": channel.name
    })