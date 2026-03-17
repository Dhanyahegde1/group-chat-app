from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Notification
from users.models import User


# Get all unread notifications for a user
@api_view(['GET'])
def get_notifications(request, user_id):
    notifications = Notification.objects.filter(
        recipient_id=user_id,
        is_read=False
    ).order_by('-created_at')

    data = []
    for n in notifications:
        data.append({
            "id": n.id,
            "sender": n.sender_username,
            "type": n.notification_type,
            "target": n.target,
            "preview": n.message_preview,
            "created_at": n.created_at.strftime("%H:%M")
        })
    return Response(data)


# Mark all notifications as read
@api_view(['POST'])
def mark_all_read(request, user_id):
    Notification.objects.filter(
        recipient_id=user_id,
        is_read=False
    ).update(is_read=True)
    return Response({"message": "All notifications marked as read"})


# Mark single notification as read
@api_view(['POST'])
def mark_read(request, notification_id):
    try:
        n = Notification.objects.get(id=notification_id)
        n.is_read = True
        n.save()
        return Response({"message": "Notification marked as read"})
    except Notification.DoesNotExist:
        return Response({"error": "Notification not found"}, status=404)