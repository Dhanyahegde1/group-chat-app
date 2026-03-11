import json
import logging
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from channels_app.models import Channel
from messaging.models import Message

logger = logging.getLogger("websocket")
User = get_user_model()


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):

        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        logger.info(f"User connected to room: {self.room_name}")

        await self.accept()

        await self.add_online_user()

        history = await self.get_chat_history()

        await self.send(text_data=json.dumps({
            "type": "chat_history",
            "messages": history
        }))


    async def disconnect(self, close_code):

        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

        await self.remove_online_user()

        logger.info(f"User disconnected from room: {self.room_name}")


    async def receive(self, text_data):

        try:
            data = json.loads(text_data)
        except json.JSONDecodeError:
            return

        event_type = data.get("type", "chat_message")

        if event_type == "chat_message":

            message = data.get("message")
            username = data.get("username")

            if not message or not username:
                return

            logger.info(f"Message received: {message}")

            await self.save_message(username, message)

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "chat_message",
                    "message": message,
                    "username": username
                }
            )

        elif event_type == "typing":

            username = data.get("username")

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "user_typing",
                    "username": username
                }
            )

        elif event_type == "read":

            message_id = data.get("message_id")

            if message_id:
                await self.mark_as_read(message_id)


    async def chat_message(self, event):

        await self.send(text_data=json.dumps({
            "type": "chat_message",
            "message": event["message"],
            "username": event["username"]
        }))


    async def user_typing(self, event):

        await self.send(text_data=json.dumps({
            "type": "typing",
            "username": event["username"]
        }))


    @database_sync_to_async
    def save_message(self, username, message):

        try:
            user = User.objects.get(username=username)
            channel = Channel.objects.get(name=self.room_name)

            Message.objects.create(
                sender=user,
                channel=channel,
                content=message
            )

        except User.DoesNotExist:
            logger.error(f"User not found: {username}")

        except Channel.DoesNotExist:
            logger.error(f"Channel not found: {self.room_name}")


    @database_sync_to_async
    def get_chat_history(self):

        try:
            channel = Channel.objects.get(name=self.room_name)

            messages = Message.objects.filter(channel=channel).order_by("timestamp")

            history = []

            for msg in messages:
                history.append({
                    "username": msg.sender.username,
                    "message": msg.content
                })

            return history

        except Channel.DoesNotExist:
            logger.error(f"Channel not found: {self.room_name}")
            return []


    @database_sync_to_async
    def add_online_user(self):

        try:
            channel = Channel.objects.get(name=self.room_name)
            logger.info(f"User joined channel {channel.name}")

        except Channel.DoesNotExist:
            logger.error(f"Channel not found: {self.room_name}")


    @database_sync_to_async
    def remove_online_user(self):

        try:
            channel = Channel.objects.get(name=self.room_name)
            logger.info(f"User left channel {channel.name}")

        except Channel.DoesNotExist:
            logger.error(f"Channel not found: {self.room_name}")


    @database_sync_to_async
    def mark_as_read(self, message_id):

        try:
            msg = Message.objects.get(id=message_id)
            msg.is_read = True
            msg.save()

        except Message.DoesNotExist:
            logger.error(f"Message not found: {message_id}")