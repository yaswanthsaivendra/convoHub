import json
from django.contrib.auth.models import User
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async

from .models import Room, Message
from rooms.nltk_tagging import process_message

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f"chat_{self.room_name}"
        username = self.scope['user']

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': 'has joined',
                'category' : 'joining',
                'is_fog' : False,
                'username': str(username)
            }
        )

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        data = json.loads(text_data)
        print(data)
        message = data['message']
        username = data['username']
        room = data['room']

        is_fog = False

        if message[0:3].lower() == 'fog':
            is_fog = True
            message = message[3:]
            await self.save_message(username, room, message, True)
        else:
            await self.save_message(username, room, message)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'category' : 'message',
                'is_fog' : is_fog,
                'message': message,
                'username': username
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        category = event['category']
        message = event['message']
        username = event['username']
        is_fog = event['is_fog']

        # Send message to WebSocket
        if is_fog:
            message = process_message(message)

        await self.send(text_data=json.dumps({
            'category' : category,
            'message': message,
            'username': username,
            'is_fog' : is_fog
        }))

    @sync_to_async
    def save_message(self, username, room, message, is_fog=False):
        user = User.objects.get(username=username)
        room = Room.objects.get(slug=room)

        Message.objects.create(user=user, room=room, content=message, is_fog=is_fog)