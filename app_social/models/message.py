from datetime import timedelta

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from .thread import Thread

User = settings.AUTH_USER_MODEL


class Message(models.Model):
    """
    Represents a single message within a chat thread.

    Behavior:
        - Automatically updates the thread's `updated_at` timestamp when a message is saved.
    """

    thread = models.ForeignKey(
        Thread, on_delete=models.CASCADE, related_name="messages"
    )
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="sent_messages"
    )
    content = models.CharField(max_length=400)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        Thread.objects.filter(id=self.thread.id).update(updated_at=timezone.now())

    def __str__(self):
        return f"{self.sender.mc_username}: {self.content[:30]}"
