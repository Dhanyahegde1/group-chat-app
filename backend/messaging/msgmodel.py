from django.db import models
from users.models import User
from channels_app.models import Channel


class Message(models.Model):

    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender} : {self.content[:30]}"