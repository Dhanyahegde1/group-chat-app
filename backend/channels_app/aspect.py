from rest_framework.decorators import api_view
from rest_framework.response import Response
from .chanels import Channel, ChannelMember, ChannelInvite
from users.models import User


@api_view(['POST'])
def generate_invite(request):
    channel_id = request.data.get('channel_id')
    try:
        channel = Channel.objects.get(id=channel_id)
        invite = ChannelInvite.objects.create(channel=channel)
        
        # Get the host IP from the request so it works on any network
        host = request.get_host().split(':')[0]  # gets your machine's IP
        invite_link = f"http://{host}:3001/join/{invite.code}"
        
        return Response({"invite_link": invite_link})
    except Channel.DoesNotExist:
        return Response({"error": "Channel not found"}, status=404)


@api_view(['POST'])
def request_join(request, code):
    username = request.data.get('username')
    try:
        invite = ChannelInvite.objects.get(code=code, status='pending')
        user = User.objects.get(username=username)
        invite.invited_user = user
        invite.save()
        return Response({"message": "Join request sent, waiting for host approval"})
    except ChannelInvite.DoesNotExist:
        return Response({"error": "Invalid or expired invite"}, status=404)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=404)


@api_view(['POST'])
def respond_invite(request):
    code = request.data.get('code')
    action = request.data.get('action')  # 'accept' or 'decline'
    try:
        invite = ChannelInvite.objects.get(code=code, status='pending')
        if action == 'accept':
            ChannelMember.objects.get_or_create(
                user=invite.invited_user,
                channel=invite.channel
            )
            invite.status = 'accepted'
        else:
            invite.status = 'declined'
        invite.save()
        return Response({"message": f"Invite {invite.status}"})
    except ChannelInvite.DoesNotExist:
        return Response({"error": "Invite not found"}, status=404)
    
@api_view(['GET'])
def check_invite_status(request, code):
    try:
        invite = ChannelInvite.objects.get(code=code)
        return Response({"status": invite.status})
    except ChannelInvite.DoesNotExist:
        return Response({"error": "Invite not found"}, status=404)
    
@api_view(['GET'])
def get_pending_invite(request, channel_id):
    try:
        invite = ChannelInvite.objects.filter(
            channel_id=channel_id,
            status='pending',
            invited_user__isnull=False
        ).first()
        if invite:
            return Response({
                "code": str(invite.code),
                "username": invite.invited_user.username
            })
        return Response({})
    except Exception as e:
        return Response({"error": str(e)}, status=400)   