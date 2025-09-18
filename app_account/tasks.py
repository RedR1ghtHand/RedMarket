from datetime import timedelta

from celery import shared_task
from django.utils import timezone

from .models import User


@shared_task
def update_user_online_status():
    """
    Celery Beat task to check user activity every 15 minutes.
    Sets is_online=False and clears manual status for users inactive for >15 minutes.
    """
    cutoff_time = timezone.now() - timedelta(minutes=15)
    
    inactive_users = User.objects.filter(
        last_seen_at__lt=cutoff_time,
        is_online=True
    )
    
    updated_count = 0
    for user in inactive_users:
        user.mark_offline()
        updated_count += 1
    
    return f"Updated {updated_count} users to offline status"
