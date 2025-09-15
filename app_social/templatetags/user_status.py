from datetime import timedelta

from django import template
from django.utils import timezone

register = template.Library()


@register.filter
def user_status(user):
    if hasattr(user, 'manual_status') and user.manual_status:
        if user.manual_status == 'idle':
            return 'idle'
        elif user.manual_status == 'invisible':
            return 'invisible'
    
    if not user.last_seen_at:
        return 'offline'

    now = timezone.now()
    time_difference = now - user.last_seen_at

    if time_difference < timedelta(minutes=5):
        return 'online'
    elif time_difference < timedelta(minutes=15):
        return 'idle'
    else:
        return 'offline'

    
@register.filter
def user_status_class(user):
    status = user_status(user)
    
    status_classes = {
        "online": "bg-success",
        "idle": "bg-warning",
        "offline": "bg-secondary",
        "invisible": "bg-secondary"
    }
    
    return status_classes.get(status, "bg-secondary")


@register.filter
def user_status_tooltip(user):
    status = user_status(user)
    
    tooltips = {
        "online": "Online",
        "idle": "Idle", 
        "offline": "Offline",
        "invisible": "Offline"
    }
    
    return tooltips.get(status, "Offline")


@register.filter
def user_status_border_class(user):
    status = user_status(user)

    border_classes = {
        "online": "border-success border-2",
        "idle": "border-warning border-2", 
        "offline": "border-secondary border-2",
        "invisible": "border-secondary border-2"
    }
    
    return border_classes.get(status, "border-secondary border-2")


@register.filter
def get_item(dictionary, key):
    """Template filter to get dictionary item by key"""
    if isinstance(dictionary, dict):
        return dictionary.get(key)
    return None


@register.filter
def get_unread_count(unread_counts, thread_id):
    """Template filter to get unread count for a specific thread"""
    if unread_counts and thread_id in unread_counts:
        return unread_counts[thread_id].get('count', 0)
    return 0