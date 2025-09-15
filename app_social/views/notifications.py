from django.http import JsonResponse
from django.template.loader import render_to_string


def render_toast_template(request):
    notification_data = request.GET.dict()
    
    # Add icon and header based on notification type
    notification_type = notification_data.get('type', 'system')
    
    icons = {
        'message': '✉️',
        'reputation': '⭐',
        'system': '🔔'
    }
    
    headers = {
        'message': 'New message',
        'reputation': 'Reputation received',
        'system': 'System alert'
    }
    
    notification_data['icon'] = icons.get(notification_type, '🔔')
    notification_data['header'] = headers.get(notification_type, 'System alert')
    
    html = render_to_string('social/notifications/_toast.html', {
        'notification': notification_data
    })
    
    return JsonResponse({'html': html})
