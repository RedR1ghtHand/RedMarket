from datetime import timedelta

from django.conf import settings
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone

from app_account.models import User
from app_social.forms import ReputationForm
from app_social.models import Reputation


class ReputationMixin:
    """
    Mixin to handle user-to-user reputation interactions.

    Features:
        - Provides context for showing reputation form/buttons in views (`get_reputation_context`).
        - Validates whether a user can give reputation (must be authenticated, not self, and account age >= 7 days).
        - Handles POST requests for reputation submissions (positive or negative badges).
        - Injects positive and negative badge lists from Django settings.

    Integration:
        - Use this mixin in views (e.g., DetailView) where public user profiles are shown.
        - Assumes the URL kwargs include 'mc_username' to identify the public profile's user.

    Expected settings:
        - REPUTATION_BADGES_POSITIVE: List of allowed positive badge strings.
        - REPUTATION_BADGES_NEGATIVE: List of allowed negative badge strings.
    """

    def get_reputation_context(self, request, public_user):
        current_user = request.user
        now = timezone.now()
        is_authenticated = current_user.is_authenticated
        is_own_profile = current_user == public_user
        account_too_young = (
            is_authenticated
            and hasattr(current_user, "created_at")
            and current_user.created_at >= now - timedelta(days=7)
        )

        can_repute = is_authenticated and not is_own_profile and not account_too_young

        already_repped = False
        existing_rep = None
        rep_form = None

        if can_repute:
            existing_rep = Reputation.objects.filter(
                giver=current_user, receiver=public_user
            ).first()
            already_repped = bool(existing_rep)

            if not already_repped:
                rep_form = ReputationForm()

        return {
            "can_repute": can_repute,
            "already_repped": already_repped,
            "rep_form": rep_form,
            "existing_rep": existing_rep,
            "is_authenticated": is_authenticated,
            "is_own_profile": is_own_profile,
            "account_too_young": account_too_young,
            "positive_badges": getattr(settings, "REPUTATION_BADGES_POSITIVE", []),
            "negative_badges": getattr(settings, "REPUTATION_BADGES_NEGATIVE", []),
        }

    def dispatch(self, request, *args, **kwargs):
        if request.method == "POST" and "rep_type" in request.POST:
            return self.handle_reputation_post(request, *args, **kwargs)
        return super().dispatch(request, *args, **kwargs)

    def handle_reputation_post(self, request, *args, **kwargs):
        rep_type = request.POST.get("rep_type")
        is_negative = rep_type == "report"
        public_user = get_object_or_404(User, mc_username=kwargs.get("mc_username"))
        current_user = request.user

        if not current_user.is_authenticated or current_user == public_user:
            messages.error(request, "Invalid reputation action.")
            return redirect(request.path)

        form = ReputationForm(request.POST, is_negative=is_negative)

        if form.is_valid():
            badge = form.cleaned_data["badge"]
            Reputation.objects.create(
                giver=current_user,
                receiver=public_user,
                badge=badge,
                is_negative=is_negative,
            )
            messages.success(request, "Reputation submitted successfully.")
        else:
            messages.error(request, "Error submitting reputation.")

        return redirect(request.path)
