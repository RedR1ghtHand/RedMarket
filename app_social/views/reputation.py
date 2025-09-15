from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.utils.functional import cached_property
from django.views.generic import ListView

from app_account.models import User
from app_social.mixins.reputation import ReputationMixin
from app_social.models import Reputation
from app_social.services.notification_service import NotificationService


class ReputationHandlerView(ReputationMixin, ListView):
    model = Reputation
    template_name = "account/reputation/base.html"
    context_object_name = "reputation_list"
    paginate_by = 10

    @property
    def mc_username(self):
        return self.kwargs["mc_username"]

    @cached_property
    def public_user(self):
        username = self.mc_username
        if not username:
            raise ValueError("mc_username is required for resolving public user")
        return get_object_or_404(User, mc_username=username)

    def get_queryset(self):
        return (
            Reputation.objects.filter(receiver=self.public_user)
            .select_related("giver")
            .order_by("-created_at")
        )

    def get_htmx_template(self, partial):
        partial_templates = {
            "reputation": "account/reputation/_reputation_form.html",
            "report": "account/reputation/_reputation_form.html",
            "rows": "account/reputation/_reputation_list.html",
            "body": "account/reputation/_body.html",
        }
        return partial_templates.get(partial, self.template_name)

    def get_template_names(self):
        if self.request.htmx:
            return [
                self.get_htmx_template(self.request.headers.get("HX-Request-Partial"))
            ]
        return [self.template_name]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        public_user = self.public_user

        rep_context = self.get_reputation_context(self.request, public_user)
        context.update(rep_context)

        partial = self.request.headers.get("HX-Request-Partial")
        context["is_negative"] = partial == "report"

        context["public_user"] = public_user

        return context

    def post(self, request, *args, **kwargs):
        public_user = self.public_user
        current_user = request.user

        if current_user == public_user:
            return HttpResponse("Cannot give reputation to yourself", status=400)

        existing_rep = Reputation.objects.filter(
            giver=current_user, receiver=public_user
        ).first()
        if existing_rep:
            return HttpResponse("Already gave reputation to this user", status=400)

        badge = request.POST.get("badge")
        is_negative = request.POST.get("is_negative") == "true"

        valid_badges = getattr(
            settings,
            (
                "REPUTATION_BADGES_NEGATIVE"
                if is_negative
                else "REPUTATION_BADGES_POSITIVE"
            ),
            [],
        )
        if badge not in valid_badges:
            return HttpResponse("Invalid badge", status=400)

        reputation = Reputation.objects.create(
            giver=current_user,
            receiver=public_user,
            badge=badge,
            is_negative=is_negative,
        )
        
        # Send notification to the user who received reputation
        NotificationService.send_reputation_notification(
            user_id=public_user.id,
            reputation=reputation,
            giver=current_user
        )

        context = self.get_reputation_context(request, public_user)
        context["public_user"] = public_user

        html = render_to_string(
            "account/public_profile/_user_card.html", context, request=request
        )

        return HttpResponse(html)
