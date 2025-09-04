from datetime import timedelta

from django.db import models
from django.utils import timezone


class UserStatusMixin(models.Model):
    last_seen_at = models.DateTimeField(default=timezone.now)
    is_online = models.BooleanField(default=False)
    manual_status = models.CharField(
        max_length=20,
        choices=[
            ('', 'Auto'),
            ('idle', 'Idle'),
            ('invisible', 'Invisible'),
        ],
        blank=True,
        default=''
    )

    class Meta:
        abstract = True

    @property
    def online_status(self):
        if not self.last_seen_at:
            return "offline"

        now = timezone.now()
        time_difference = now - self.last_seen_at

        if time_difference < timedelta(minutes=5):
            return "online"
        elif time_difference < timedelta(minutes=15):
            return "idle"
        else:
            return "offline"

    def update_activity(self):
        self.last_seen_at = timezone.now()
        self.is_online = True
        self.save(update_fields=["last_seen_at", "is_online"])

    def mark_offline(self):
        self.is_online = False
        self.save(update_fields=["is_online"])

    def set_manual_status(self, status):
        valid_statuses = ['', 'idle', 'invisible']
        if status in valid_statuses:
            self.manual_status = status
            self.save(update_fields=['manual_status'])

    def clear_manual_status(self):
        self.manual_status = ''
        self.save(update_fields=['manual_status'])

    def get_valid_manual_statuses(self):
        return ['', 'idle', 'invisible']
