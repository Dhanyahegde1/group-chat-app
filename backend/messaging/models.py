from django.db import models
from users.models import User
from channels_app.models import Channel

#message sent by user inside channel
class Message(models.Model):
    #who sent msg
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    #where msg sent
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    #msg content
    content = models.TextField()
    #msg status
    is_read = models.BooleanField(default=False)
    #msg created time
    timestamp = models.DateTimeField(auto_now_add=True)

    # String representation of message object
    def __str__(self):
        return f"{self.sender} : {self.content[:30]}"

class DirectMessage(models.Model):
    sender    = models.ForeignKey(User, on_delete=models.CASCADE, related_name="dm_sent")
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="dm_received")
    content   = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read   = models.BooleanField(default=False)

    class Meta:
        ordering = ["timestamp"]

    def __str__(self):
        return f"DM {self.sender} → {self.recipient}: {self.content[:30]}"