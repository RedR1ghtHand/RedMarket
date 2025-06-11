from django.views.generic import View, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.db.models import Q

from .models import Thread, Message
from app_account.models import User


class MessageRedirectView(LoginRequiredMixin, View):
    """
    Redirects the logged-in user to an existing private message thread
    with the target user (by mc_username), or creates one if it doesn't exist.
    """
    def get_or_create_thread(self, request_user, target_user):
        """
        Returns an existing thread between two users or creates a new one if none exists.
        Returns None if the user tries to message themselves.
        """
        if request_user == target_user:
            return None

        thread = (
            Thread.objects.filter(
                Q(user1=request_user, user2=target_user) |
                Q(user1=target_user, user2=request_user)
            ).first()
        )

        if not thread:
            thread = Thread.objects.create(user1=request_user, user2=target_user)

        return thread

    def get(self, request, *args, **kwargs):
        target_user = get_object_or_404(User, mc_username=kwargs['mc_username'])
        thread = self.get_or_create_thread(request.user, target_user)
        if thread:
            return HttpResponseRedirect(reverse('thread_detail', args=[thread.pk]))
        return HttpResponseRedirect(reverse('thread_detail'))


class ThreadDetailView(TemplateView):
    template_name = "social/thread_detail.html"

    @staticmethod
    def get_thread(request, thread_id=None):
        if thread_id:
            try:
                thread = Thread.objects.get(id=thread_id)
                if request.user not in thread.participants():
                    return None
            except Thread.DoesNotExist:
                return None
        else:
            thread = Thread.threads_for_user(request.user).order_by("-updated_at").first()
        return thread

    def get(self, request, *args, **kwargs):
        thread_id = kwargs.get('thread_id')
        thread = self.get_thread(request, thread_id)
        if thread is None:
            return redirect("thread_detail")
        return super().get(request, *args, **kwargs)

    def post(self, request, thread_id=None):
        thread = self.get_thread(request, thread_id)
        if thread is None:
            return redirect("thread_detail")

        if "delete" in request.POST:
            if request.user in thread.participants():
                thread.delete()
                return redirect("thread_detail")
            else:
                return redirect("thread_detail", thread_id=thread.id)

        content = request.POST.get("content", "").strip()
        if content:
            Message.objects.create(thread=thread, sender=request.user, content=content)
        return redirect("thread_detail", thread_id=thread.id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        request = self.request
        thread_id = self.kwargs.get("thread_id")
        thread = self.get_thread(request, thread_id)

        context["thread"] = thread
        context["messages"] = thread.messages.order_by("created_at")
        context["threads"] = Thread.threads_for_user(request.user).order_by("-updated_at")
        return context
