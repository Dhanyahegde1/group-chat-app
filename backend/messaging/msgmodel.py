id="jv9t1x"
# Import Django model utilities
from django.db import models

# Import User model
from users.models import User

# Import Channel model
from channels_app.chanels import Channel


# ---------------------------------------------------
# Message Model
# ---------------------------------------------------
# Represents a chat message sent by a user inside a channel
class Message(models.Model):

    # User who sent the message
    sender = models.ForeignKey(User, on_delete=models.CASCADE)

    # Channel where the message was sent
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)

    # Actual message content
    content = models.TextField()

    # Timestamp when the message was created
    created_at = models.DateTimeField(auto_now_add=True)

    # String representation of message object
    def __str__(self):
        return self.content
