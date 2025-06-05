from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta


class Reputation(models.Model):
    """
    Represents a reputation rating from one user to another.

    Fields:
        giver: The user who gives the reputation.
        receiver: The user who receives the reputation.
        badge: A short string badge representing the reason/type of reputation.
        is_negative: Indicates if the reputation is negative (True) or positive (False).
        created_at: Timestamp when the reputation was given.

    Constraints:
        - each user can give reputation to another user only once (unique_together).
        - users cannot give reputation to themselves.
        - users must be registered for at least 7 days before giving reputation.
    """

    giver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='given_reputations')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_reputations')
    badge = models.CharField(max_length=100)
    is_negative = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('giver', 'receiver')

    def clean(self):
        if self.giver == self.receiver:
            raise ValidationError("You cannot give reputation to yourself.")
        if self.giver.created_at > timezone.now() - timedelta(days=7):
            raise ValidationError("You must be registered for at least 7 days to give reputation.")

