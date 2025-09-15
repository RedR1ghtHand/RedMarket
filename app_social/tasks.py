from celery import shared_task
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone

from .models import Message, Thread
from .services.notification_service import NotificationService

User = get_user_model()


@shared_task(bind=True, max_retries=3, default_retry_delay=5)
def create_message_task(self, thread_id, sender_id, content):
    try:
        thread = Thread.objects.get(id=thread_id)
        sender = User.objects.get(id=sender_id)
        
        if sender not in thread.participants():
            raise ValueError("User is not a participant in this thread")
        
        msg = Message.objects.create(
            thread=thread,
            sender=sender,
            content=content
        )
        
        thread.updated_at = timezone.now()
        thread.save(update_fields=['updated_at'])
        
        # Send notification to other participants
        participants = list(thread.participants())
        for participant in participants:
            if participant != sender:
                NotificationService.send_message_notification(
                    user_id=participant.id,
                    thread=thread,
                    sender=sender,
                    message_preview=content
                )
        
        return msg.id
        
    except ObjectDoesNotExist as e:
        self.update_state(state='FAILURE', meta={'error': str(e)})
        return None
    except Exception as e:
        raise self.retry(exc=e, countdown=5)
