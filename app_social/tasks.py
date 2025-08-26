from celery import shared_task
from django.contrib.auth import get_user_model
from django.utils import timezone

from .models import Thread, Message

User = get_user_model()


@shared_task(bind=True, max_retries=3)
def create_message_task(self, thread_id, sender_id, content):
    try:
        thread = Thread.objects.get(id=thread_id)
        sender = User.objects.get(id=sender_id)
        msg = Message.objects.create(
            thread=thread,
            sender=sender,
            content=content
        )

        Thread.objects.filter(id=thread.id).update(updated_at=timezone.now())
        return msg.id

    except Exception as e:
        raise self.retry(exc=e, countdown=5)
