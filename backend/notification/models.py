from django.db import models
from users.models import User

class Notification(models.Model):

    TYPE_CHOICES = [
        ('channel', 'Channel Message'),
        ('dm', 'Direct Message'),
    ]

    # Who receives the notification
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')

    # Who triggered it
    sender_username = models.CharField(max_length=150)

    # Type of notification
    notification_type = models.CharField(max_length=10, choices=TYPE_CHOICES)

    # Channel name or DM username
    target = models.CharField(max_length=255)

    # Message preview
    message_preview = models.CharField(max_length=100)

    # Read status
    is_read = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.recipient} from {self.sender_username}"