import json

from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model

from .models import Thread
from .tasks import create_message_task

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.thread_id = self.scope['url_route']['kwargs']['thread_id']
        self.thread_group_name = f'chat_{self.thread_id}'
        
        await self.channel_layer.group_add(
            self.thread_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.thread_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        content = data['content']
        user = self.scope['user']
        
        create_message_task.delay(self.thread_id, user.id, content)
        
        from django.utils import timezone
        current_time = timezone.now()
        await self.channel_layer.group_send(
            self.thread_group_name,
            {
                'type': 'chat_message',
                'message': {
                    'content': content,
                    'sender': user.mc_username,
                    'sender_id': user.id,
                    'created_at': current_time.isoformat(),
                }
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'type': 'chat_message',
            'message': event['message']
        }))
