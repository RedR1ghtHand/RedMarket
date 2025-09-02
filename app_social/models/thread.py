from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models

User = settings.AUTH_USER_MODEL


class Thread(models.Model):
    """
    Represents a private chat thread between two users.

    Constraints:
        - A thread cannot be created between the same user.
        - Only one unique thread per user pair (user1, user2) is allowed.

    Methods:
        participants(): Returns a list of the two participants.
        threads_for_user(user): Returns all threads where the given user is a participant.
        get_or_create_between(user_a, user_b): Returns existing or creates a new thread
                                               between two users (ordered by ID).
    """

    user1 = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="threads_started"
    )
    user2 = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="threads_received"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ["user1", "user2"]

    def clean(self):
        if self.user1 == self.user2:
            raise ValidationError("Cannot create thread with yourself")

    def participants(self):
        return [self.user1, self.user2]

    @staticmethod
    def threads_for_user(user):
        return Thread.objects.filter(models.Q(user1=user) | models.Q(user2=user))

    def __str__(self):
        return f"{self.user1.mc_username} 💬 {self.user2.mc_username}"

    @staticmethod
    def get_or_create_between(user_a, user_b):
        user1, user2 = sorted([user_a, user_b], key=lambda u: u.id)
        thread, created = Thread.objects.get_or_create(user1=user1, user2=user2)
        return thread
