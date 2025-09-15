from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models import Count, Q
from django.utils import timezone

from app_social.models import Notification, Thread


class NotificationService:
    @staticmethod
    def send_notification(user_id, notification_type, title, message, related_thread=None, related_reputation=None):
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        user = User.objects.get(id=user_id)
        notification = Notification.objects.create(
            user=user,
            notification_type=notification_type,
            title=title,
            message=message,
            related_thread=related_thread,
            related_reputation=related_reputation
        )
        
        NotificationService._send_websocket_notification(user_id, notification)
        return notification

    @staticmethod
    def send_message_notification(user_id, thread, sender, message_preview):
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        user = User.objects.get(id=user_id)
        notification = Notification.create_message_notification(
            user=user,
            thread=thread,
            sender=sender,
            message_preview=message_preview
        )
        
        NotificationService._send_websocket_notification(user_id, notification)
        return notification

    @staticmethod
    def send_reputation_notification(user_id, reputation, giver):
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        user = User.objects.get(id=user_id)
        notification = Notification.create_reputation_notification(
            user=user,
            reputation=reputation,
            giver=giver
        )
        
        NotificationService._send_websocket_notification(user_id, notification)
        return notification

    @staticmethod
    def send_system_notification(user_id, title, message):
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        user = User.objects.get(id=user_id)
        notification = Notification.create_system_notification(
            user=user,
            title=title,
            message=message
        )
        
        NotificationService._send_websocket_notification(user_id, notification)
        return notification

    @staticmethod
    def _send_websocket_notification(user_id, notification):
        channel_layer = get_channel_layer()
        group_name = f'notifications_{user_id}'
        
        notification_data = {
            'id': notification.id,
            'type': notification.notification_type,
            'title': notification.title,
            'message': notification.message,
            'is_read': notification.is_read,
            'created_at': notification.created_at.isoformat(),
            'related_thread_id': notification.related_thread_id,
            'related_reputation_id': notification.related_reputation_id,
        }
        
        # Add sender username for message and reputation notifications
        if notification.notification_type in ['message', 'reputation']:
            if notification.related_thread:
                # For message notifications, get sender from the thread
                participants = list(notification.related_thread.participants())
                for participant in participants:
                    if participant.id != user_id:
                        notification_data['sender_username'] = participant.mc_username
                        break
            elif notification.related_reputation:
                # For reputation notifications, get giver from the reputation
                notification_data['sender_username'] = notification.related_reputation.giver.mc_username
        
        # Get unread counts for all threads for this user
        unread_counts = NotificationService._get_unread_counts(user_id)
        
        async_to_sync(channel_layer.group_send)(
            group_name,
            {
                'type': 'notification_message',
                'notification': notification_data,
                'unread_counts': unread_counts
            }
        )

    @staticmethod
    def _get_unread_counts(user_id):
        """Get unread message notification counts per thread for a user"""
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        user = User.objects.get(id=user_id)
        threads = Thread.threads_for_user(user)
        
        unread_counts = {}
        for thread in threads:
            count = Notification.objects.filter(
                user=user,
                notification_type='message',
                related_thread=thread,
                is_read=False
            ).count()
            
            if count > 0:
                # Get the other participant's username for this thread
                for participant in thread.participants():
                    if participant != user:
                        unread_counts[str(thread.id)] = {
                            'count': count,
                            'participant_username': participant.mc_username
                        }
                        break
        
        return unread_counts

    @staticmethod
    def mark_thread_notifications_read(user_id, thread_id):
        """Mark all message notifications for a specific thread as read"""
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        user = User.objects.get(id=user_id)
        thread = Thread.objects.get(id=thread_id)
        
        notifications = Notification.objects.filter(
            user=user,
            notification_type='message',
            related_thread=thread,
            is_read=False
        )
        
        for notification in notifications:
            notification.mark_as_read()
        
        # Send updated unread counts
        unread_counts = NotificationService._get_unread_counts(user_id)
        channel_layer = get_channel_layer()
        group_name = f'notifications_{user_id}'
        
        async_to_sync(channel_layer.group_send)(
            group_name,
            {
                'type': 'unread_counts_update',
                'unread_counts': unread_counts
            }
        )
