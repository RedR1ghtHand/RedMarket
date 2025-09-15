from django.conf import settings
from django.db import models
from django.utils import timezone

User = settings.AUTH_USER_MODEL


class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('message', 'New Message'),
        ('reputation', 'Reputation'),
        ('system', 'System Notification'),
    ]

    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='notifications'
    )
    notification_type = models.CharField(
        max_length=20, 
        choices=NOTIFICATION_TYPES,
        default='system'
    )
    title = models.CharField(max_length=100)
    message = models.TextField(max_length=500)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(null=True, blank=True)
    
    # Optional foreign keys for related objects
    related_thread = models.ForeignKey(
        'Thread', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        related_name='notifications'
    )
    related_reputation = models.ForeignKey(
        'Reputation', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        related_name='notifications'
    )
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'is_read']),
            models.Index(fields=['user', 'notification_type']),
            models.Index(fields=['created_at']),
        ]

    def mark_as_read(self):
        if not self.is_read:
            self.is_read = True
            self.read_at = timezone.now()
            self.save(update_fields=['is_read', 'read_at'])

    def __str__(self):
        return f"{self.user.mc_username} - {self.title}"

    @classmethod
    def create_message_notification(cls, user, thread, sender, message_preview):
        return cls.objects.create(
            user=user,
            notification_type='message',
            title="New message",
            message=message_preview[:100] + "..." if len(message_preview) > 100 else message_preview,
            related_thread=thread
        )

    @classmethod
    def create_reputation_notification(cls, user, reputation, giver):
        return cls.objects.create(
            user=user,
            notification_type='reputation',
            title=f"Received {reputation.badge} reputation",
            message=f"Reputation: {reputation.badge}",
            related_reputation=reputation
        )

    @classmethod
    def create_system_notification(cls, user, title, message):
        return cls.objects.create(
            user=user,
            notification_type='system',
            title=title,
            message=message
        )
