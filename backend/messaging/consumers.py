import json
import logging
from channels.generic.websocket import AsyncWebsocketConsumer

logger = logging.getLogger("websocket")


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):

        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        logger.info(f"User connected to room: {self.room_name}")

        await self.accept()

    async def disconnect(self, close_code):

        logger.info(f"User disconnected from room: {self.room_name}")

    async def receive(self, text_data):

        data = json.loads(text_data)
        message = data["message"]

        logger.info(f"Message received: {message}")

        await self.send(text_data=json.dumps({
            "message": message
        }))