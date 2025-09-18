import json

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model

from .models import Notification, Thread
from .tasks import create_message_task

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.thread_id = self.scope['url_route']['kwargs']['thread_id']
        user = self.scope['user']
        
        if not user.is_authenticated:
            await self.close()
            return
        
        try:
            thread = await sync_to_async(Thread.objects.get)(id=self.thread_id)
            participants = await sync_to_async(thread.participants)()
            if user not in participants:
                await self.close()
                return
        except Thread.DoesNotExist:
            await self.close()
            return
        
        self.thread_group_name = f'chat_{self.thread_id}'
        await self.channel_layer.group_add(
            self.thread_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        if hasattr(self, 'thread_group_name'):
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


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user = self.scope['user']
        
        if not user.is_authenticated:
            await self.close()
            return
        
        self.user_id = user.id
        self.notification_group_name = f'notifications_{self.user_id}'
        
        await self.channel_layer.group_add(
            self.notification_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        if hasattr(self, 'notification_group_name'):
            await self.channel_layer.group_discard(
                self.notification_group_name,
                self.channel_name
            )

    async def receive(self, text_data):
        data = json.loads(text_data)
        action = data.get('action')
        
        if action == 'mark_read':
            notification_id = data.get('notification_id')
            if notification_id:
                await self.mark_notification_read(notification_id)
        elif action == 'mark_thread_read':
            thread_id = data.get('thread_id')
            if thread_id:
                await self.mark_thread_read(thread_id)
        elif action == 'get_unread_counts':
            await self.send_unread_counts()

    async def mark_notification_read(self, notification_id):
        try:
            notification = await sync_to_async(Notification.objects.get)(
                id=notification_id, 
                user_id=self.user_id
            )
            await sync_to_async(notification.mark_as_read)()
        except Notification.DoesNotExist:
            pass

    async def mark_thread_read(self, thread_id):
        from .services.notification_service import NotificationService
        await sync_to_async(NotificationService.mark_thread_notifications_read)(
            self.user_id, thread_id
        )

    async def send_unread_counts(self):
        from .services.notification_service import NotificationService
        unread_counts = await sync_to_async(NotificationService._get_unread_counts)(
            self.user_id
        )
        await self.send(text_data=json.dumps({
            'type': 'unread_counts',
            'unread_counts': unread_counts
        }))

    async def notification_message(self, event):
        message_data = {
            'type': 'notification',
            'notification': event['notification']
        }
        
        # Include unread counts if available
        if 'unread_counts' in event:
            message_data['unread_counts'] = event['unread_counts']
        
        await self.send(text_data=json.dumps(message_data))

    async def unread_counts_update(self, event):
        await self.send(text_data=json.dumps({
            'type': 'unread_counts',
            'unread_counts': event['unread_counts']
        }))
