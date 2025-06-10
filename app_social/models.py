from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta

User = settings.AUTH_USER_MODEL


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
    giver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='given_reputations')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_reputations')
    badge = models.CharField(max_length=100)
    is_negative = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('giver', 'receiver')

    @staticmethod
    def get_score_for_user(user):
        """
        Calculate the net reputation score for the given user.

        :param user: A user model instance whose reputation score is to be calculated.
        :return: The reputation score as (positive count) - (negative count).
        """
        agg = Reputation.objects.filter(receiver=user).aggregate(
            pos=models.Count('id', filter=models.Q(is_negative=False)),
            neg=models.Count('id', filter=models.Q(is_negative=True)),
        )
        return (agg['pos'] or 0) - (agg['neg'] or 0)

    def clean(self):
        if self.giver == self.receiver:
            raise ValidationError("You cannot give reputation to yourself.")
        if self.giver.created_at > timezone.now() - timedelta(days=7):
            raise ValidationError("You must be registered for at least 7 days to give reputation.")


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
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="threads_started")
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="threads_recieved")
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


class Message(models.Model):
    """
    Represents a single message within a chat thread.

    Behavior:
        - Automatically updates the thread's `updated_at` timestamp when a message is saved.
    """
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")
    content = models.CharField(max_length=400)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.thread.updated_at = timezone.now()
        self.thread.save(update_fields=['updated_at'])

    def __str__(self):
        return f"{self.sender.mc_username}: {self.content[:30]}"
