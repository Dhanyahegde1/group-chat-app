# Import Django model utilities
from django.db import models

# Import the custom User model
from users.models import User
import uuid

# Represents a chat channel/group where users can communicate
class Channel(models.Model):

    # Name of the chat channel
    name = models.CharField(max_length=255)

    # User who created the channel
    # If the creator is deleted, the channel will also be deleted
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    # Timestamp when the channel was created
    created_at = models.DateTimeField(auto_now_add=True)

    is_private = models.BooleanField(default=False)

    # String representation (shown in Django admin / querysets)
    def __str__(self):
        return self.name


# ---------------------------------------------------
# Channel Member Model
# ---------------------------------------------------
# Represents membership of users inside channels
class ChannelMember(models.Model):

    # User who joined the channel
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # Channel the user joined
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)

    # Timestamp when the user joined the channel
    joined_at = models.DateTimeField(auto_now_add=True)

    # Prevents duplicate membership
    # A user cannot join the same channel multiple times
    class Meta:
        unique_together = ('user', 'channel')

    # String representation for admin/debugging
    def __str__(self):
        return f"{self.user} -> {self.channel}"
    
    
class ChannelInvite(models.Model):

    # Which channel the invite is for
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)

    # Unique invite code
    code = models.UUIDField(default=uuid.uuid4, unique=True)

    # Who was invited (null until someone uses the link)
    invited_user = models.ForeignKey(
        User, null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='invites'
    )

    # Status of invite
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('declined', 'Declined'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')