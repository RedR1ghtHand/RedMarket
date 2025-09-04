from datetime import timedelta

from django import template
from django.utils import timezone
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def user_status(user):
    if hasattr(user, 'manual_status') and user.manual_status:
        if user.manual_status == 'idle':
            return {
                "status": "idle",
                "class": "bg-warning",
                "tooltip": "Idle"
            }
        elif user.manual_status == 'invisible':
            return {
                "status": "invisible",
                "class": "bg-secondary",
                "tooltip": "Offline"
            }
    
    if not user.last_seen_at:
        return {
            "status": "offline",
            "class": "bg-secondary",
            "tooltip": "Offline"
        }

    now = timezone.now()
    time_difference = now - user.last_seen_at

    if time_difference < timedelta(minutes=5):
        return {
            "status": "online",
            "class": "bg-success",
            "tooltip": "Online"
        }
    elif time_difference < timedelta(minutes=15):
        return {
            "status": "idle",
            "class": "bg-warning",
            "tooltip": "Idle"
        }
    else:
        return {
            "status": "offline",
            "class": "bg-secondary",
            "tooltip": "Offline"
        }

    
@register.simple_tag
def user_status_icon(user, size=12):
    status_data = user_status(user)

    html = f'''
    <div class="position-absolute bottom-0 end-0 {status_data['class']} rounded-circle border border-white"
         style="width: {size}px; height: {size}px;" 
         title="{status_data['tooltip']}">
    </div>
    '''
    
    return mark_safe(html)