from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.views.generic import View


class SetUserStatusView(LoginRequiredMixin, View):
    template_name = 'social/messages/_status_dropdown.html'
    
    def post(self, request, *args, **kwargs):
        status = request.POST.get('status', '')
        
        if status not in request.user.get_valid_manual_statuses():
            return HttpResponse('Invalid status', status=400)
        
        request.user.set_manual_status(status)
        
        html = render_to_string(self.template_name, {}, request=request)
        return HttpResponse(html)
