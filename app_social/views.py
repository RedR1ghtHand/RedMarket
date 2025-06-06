from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.utils import timezone
from django.conf import settings
from datetime import timedelta

from .models import Reputation
from app_account.models import User
from .forms import ReputationForm


class ReputationMixin:
    """
    Mixin to handle user-to-user reputation interactions.

    Features:
        - Provides context for showing reputation form/buttons in views (`get_reputation_context`).
        - Returns all Reputation entries received by the given user (`get_reputation_queryset`).
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
        """Returns context dict for reputation logic."""
        current_user = request.user
        now = timezone.now()
        can_repute = (
            current_user.is_authenticated
            and current_user != public_user
            and hasattr(current_user, 'created_at')
            and current_user.created_at < now - timedelta(days=7)
        )

        already_repped = False
        existing_rep = None
        rep_form = None

        if can_repute:
            existing_rep = Reputation.objects.filter(giver=current_user, receiver=public_user).first()
            already_repped = bool(existing_rep)

            if not already_repped:
                rep_form = ReputationForm()

        return {
            'can_repute': can_repute,
            'already_repped': already_repped,
            'rep_form': rep_form,
            'existing_rep': existing_rep,
            'positive_badges': getattr(settings, 'REPUTATION_BADGES_POSITIVE', []),
            'negative_badges': getattr(settings, 'REPUTATION_BADGES_NEGATIVE', []),
        }

    def get_reputation_queryset(self, user):
        return Reputation.objects.filter(receiver=user).select_related('giver').order_by('-created_at')

    def dispatch(self, request, *args, **kwargs):
        """Override dispatch to intercept POST if it's a rep submission."""
        if request.method == 'POST' and 'rep_type' in request.POST:
            return self.handle_reputation_post(request, *args, **kwargs)
        return super().dispatch(request, *args, **kwargs)

    def handle_reputation_post(self, request, *args, **kwargs):
        """Handles the submission of a reputation form (positive or negative)."""
        rep_type = request.POST.get('rep_type')
        is_negative = rep_type == 'report'
        public_user = get_object_or_404(User, mc_username=kwargs.get('mc_username'))
        current_user = request.user

        if not current_user.is_authenticated or current_user == public_user:
            messages.error(request, "Invalid reputation action.")
            return redirect(request.path)

        form = ReputationForm(request.POST, is_negative=is_negative)

        if form.is_valid():
            badge = form.cleaned_data['badge']
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
