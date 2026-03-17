import json
import logging
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from channels_app.chanels import Channel, ChannelMember
from messaging.models import Message, DirectMessage

logger = logging.getLogger("websocket")
User = get_user_model()


 
class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_name       = self.scope["url_route"]["kwargs"]["room_name"]
        self.username        = self.scope["url_route"]["kwargs"]["username"]
        self.room_group_name = f"chat_{self.room_name}"

        # ── MEMBERSHIP GATE ──────────────────────────────────────────────────
        if not await self.check_membership(self.username, self.room_name):
            logger.warning(f"'{self.username}' blocked from '{self.room_name}' - not a member")
            await self.close(code=4003)
            return
        # ────────────────────────────────────────────────────────────────────

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        await self.mark_messages_read()
        await self.channel_layer.group_send(
            self.room_group_name,
            {"type": "messages_read", "username": self.username}
        )
        await self.channel_layer.group_send(
            self.room_group_name,
            {"type": "user_online", "username": self.username}
        )

        history = await self.get_chat_history()
        await self.send(text_data=json.dumps({"type": "chat_history", "messages": history}))
        logger.info(f"'{self.username}' connected to room '{self.room_name}'")


    async def disconnect(self, close_code):
        if not hasattr(self, "room_group_name"):
            return  # was rejected before group_add

        await self.channel_layer.group_send(
            self.room_group_name,
            {"type": "user_offline", "username": getattr(self, "username", "")}
        )
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        logger.info(f"'{getattr(self, 'username', '?')}' disconnected from '{self.room_name}'")


    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
        except json.JSONDecodeError:
            return

        event_type = data.get("type", "chat_message")

        if event_type == "chat_message":
            message  = data.get("message")
            username = data.get("username") or self.username
            if not message:
                return
            if not await self.check_membership(username, self.room_name):
                return
            await self.save_message(username, message)
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type":      "chat_message",
                    "message":   message,
                    "username":  username,
                    "timestamp": __import__("datetime").datetime.now().strftime("%H:%M"),
                }
            )

        elif event_type == "join":
            username = data.get("username")
            self.username = username
            await self.channel_layer.group_send(
                self.room_group_name,
                {"type": "user_online", "username": username}
            )

        elif event_type == "typing":
            await self.channel_layer.group_send(
                self.room_group_name,
                {"type": "user_typing", "username": data.get("username")}
            )

        elif event_type == "read":
            message_id = data.get("message_id")
            if message_id:
                await self.mark_as_read(message_id)


    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            "type": "chat_message", "message": event["message"],
            "username": event["username"], "timestamp": event.get("timestamp", ""),
        }))

    async def user_typing(self, event):
        await self.send(text_data=json.dumps({"type": "typing", "username": event["username"]}))

    async def messages_read(self, event):
        await self.send(text_data=json.dumps({"type": "messages_read"}))

    async def user_online(self, event):
        await self.send(text_data=json.dumps({"type": "user_online", "username": event["username"]}))

    async def user_offline(self, event):
        await self.send(text_data=json.dumps({"type": "user_offline", "username": event["username"]}))


    @database_sync_to_async
    def check_membership(self, username, room_name):
        return ChannelMember.objects.filter(
            user__username=username,
            channel__name=room_name
        ).exists()

    @database_sync_to_async
    def mark_messages_read(self):
        try:
            channel = Channel.objects.get(name=self.room_name)
            Message.objects.filter(channel=channel, is_read=False).update(is_read=True)
        except Channel.DoesNotExist:
            pass

    @database_sync_to_async
    def save_message(self, username, message):
        try:
            user    = User.objects.get(username=username)
            channel = Channel.objects.get(name=self.room_name)
            Message.objects.create(sender=user, channel=channel, content=message)

            # ← notifications for all members except sender
            from notification.models import Notification
            members = ChannelMember.objects.filter(channel=channel).exclude(user=user)
            for member in members:
                Notification.objects.create(
                    recipient=member.user,
                    sender_username=username,
                    notification_type='channel',
                    target=self.room_name,
                    message_preview=message[:100]
                )
        except (User.DoesNotExist, Channel.DoesNotExist) as e:
            logger.error(f"save_message error: {e}")

    @database_sync_to_async
    def get_chat_history(self):
        try:
            channel  = Channel.objects.get(name=self.room_name)
            messages = Message.objects.filter(channel=channel).order_by("timestamp")
            return [
                {"username": m.sender.username, "message": m.content, "timestamp": m.timestamp.strftime("%H:%M")}
                for m in messages
            ]
        except Channel.DoesNotExist:
            return []

    @database_sync_to_async
    def mark_messages_read(self):
        try:
            channel = Channel.objects.get(name=self.room_name)
            Message.objects.filter(channel=channel, is_read=False).update(is_read=True)
        except Channel.DoesNotExist:
            pass

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


# ─────────────────────────────────────────────────────────────────────────────
# DIRECT MESSAGE CONSUMER
# URL: ws://…/ws/dm/<my_username>/<other_username>/
# ─────────────────────────────────────────────────────────────────────────────
class DMConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        kwargs              = self.scope["url_route"]["kwargs"]
        self.my_username    = kwargs["my_username"]
        self.other_username = kwargs["other_username"]

        # Canonical group name — alphabetically sorted so both users share same group
        names              = sorted([self.my_username, self.other_username])
        self.dm_group_name = f"dm_{'__'.join(names)}"

        await self.channel_layer.group_add(self.dm_group_name, self.channel_name)
        await self.accept()

        await self.mark_dm_read()

        history = await self.get_dm_history()
        await self.send(text_data=json.dumps({"type": "dm_history", "messages": history}))
        logger.info(f"DM connected: {self.my_username} ↔ {self.other_username}")


    async def disconnect(self, close_code):
        if hasattr(self, "dm_group_name"):
            await self.channel_layer.group_discard(self.dm_group_name, self.channel_name)


    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
        except json.JSONDecodeError:
            return

        event_type = data.get("type", "dm_message")

        if event_type == "dm_message":
            message = data.get("message", "").strip()
            if not message:
                return
            dm = await self.save_dm(message)
            if not dm:
                return
            await self.channel_layer.group_send(
                self.dm_group_name,
                {
                    "type":      "dm_message",
                    "message":   message,
                    "sender":    self.my_username,
                    "timestamp": __import__("datetime").datetime.now().strftime("%H:%M"),
                    "dm_id":     dm["id"],
                }
            )

        elif event_type == "typing":
            await self.channel_layer.group_send(
                self.dm_group_name,
                {"type": "dm_typing", "sender": self.my_username}
            )

        elif event_type == "read":
            await self.mark_dm_read()


    async def dm_message(self, event):
        await self.send(text_data=json.dumps({
            "type":      "dm_message",
            "message":   event["message"],
            "sender":    event["sender"],
            "timestamp": event.get("timestamp", ""),
            "dm_id":     event.get("dm_id"),
        }))

    async def dm_typing(self, event):
        if event["sender"] != self.my_username:  # don't echo back to sender
            await self.send(text_data=json.dumps({"type": "typing", "sender": event["sender"]}))


    @database_sync_to_async
    def save_dm(self, content):
        try:
            sender    = User.objects.get(username=self.my_username)
            recipient = User.objects.get(username=self.other_username)
            dm = DirectMessage.objects.create(sender=sender, recipient=recipient, content=content)
            
            # ← notification for recipient
            from notification.models import Notification
            Notification.objects.create(
                recipient=recipient,
                sender_username=self.my_username,
                notification_type='dm',
                target=self.my_username,
                message_preview=content[:100]
            )
            
            return {"id": dm.id}
        except User.DoesNotExist as e:
            logger.error(f"DM save failed: {e}")
            return None

    @database_sync_to_async
    def get_dm_history(self):
        try:
            me    = User.objects.get(username=self.my_username)
            other = User.objects.get(username=self.other_username)
        except User.DoesNotExist:
            return []
        messages = (
            DirectMessage.objects.filter(sender=me, recipient=other) |
            DirectMessage.objects.filter(sender=other, recipient=me)
        ).order_by("timestamp")
        return [
            {
                "sender":    m.sender.username,
                "message":   m.content,
                "timestamp": m.timestamp.strftime("%H:%M"),
                "is_read":   m.is_read,
                "dm_id":     m.id,
            }
            for m in messages
        ]

    @database_sync_to_async
    def mark_dm_read(self):
        try:
            me    = User.objects.get(username=self.my_username)
            other = User.objects.get(username=self.other_username)
            DirectMessage.objects.filter(sender=other, recipient=me, is_read=False).update(is_read=True)
        except User.DoesNotExist:
            pass