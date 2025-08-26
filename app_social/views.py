from django.views.generic import View, TemplateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.db.models import Q

from .models import Thread, Message
from app_account.models import User
from .tasks import create_message_task

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


class ThreadDetailView(ListView):
    model = Message
    template_name = "social/messages/base.html"
    paginate_by = 10

    def get_thread(self):
        thread_id = self.kwargs.get("thread_id")
        if thread_id:
            try:
                thread = Thread.objects.get(id=thread_id)
                if self.request.user not in thread.participants():
                    return None
            except Thread.DoesNotExist:
                return None
        else:
            thread = Thread.threads_for_user(self.request.user).order_by("-updated_at").first()
        return thread

    def get_queryset(self):
        self.thread = self.get_thread()
        if not self.thread:
            return Message.objects.none()
        return (
            self.thread.messages
            .order_by("-created_at")
        )

    def get_htmx_template(self, partial):
        partial_templates = {
            "threads": "social/messages/_threads_list.html",
            "container": "social/messages/_thread_container.html",
            "body": "social/messages/_body.html",
        }
        return partial_templates.get(partial, self.template_name)

    def get_template_names(self):
        if self.request.htmx:
            return [self.get_htmx_template(self.request.headers.get("HX-Request-Partial"))]
        return [self.template_name]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        page = context["page_obj"]
        messages = list(page.object_list)[::-1]

        context.update({
            "thread": self.thread,
            "threads": Thread.threads_for_user(self.request.user).order_by("-updated_at"),
            "messages": messages,
            "page_obj": page,
            "is_paginated": context["is_paginated"],
        })
        return context

    def get(self, request, *args, **kwargs):
        self.thread = self.get_thread()
        if self.thread is None and "thread_id" in kwargs:
            return redirect("thread_detail")
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.thread = self.get_thread()
        if self.thread is None:
            return redirect("thread_detail")

        if "delete" in request.POST:
            if request.user in self.thread.participants():
                self.thread.delete()
            return redirect("thread_detail")

        content = request.POST.get("content", "").strip()
        if content:
            create_message_task.delay(self.thread.id, request.user.id, content)

        return redirect("thread_detail", thread_id=self.thread.id)