import pytest
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta

from app_social.models import Reputation

User = get_user_model()


@pytest.mark.django_db
class TestReputationModel:
    @pytest.fixture(autouse=True)
    def setup_users(self, user1, user2):
        self.giver = user1
        self.receiver = user2

        self.too_new_user = User.objects.create_user(
            email="new@example.com", username="new", mc_username="new_mc", password="pass"
        )
        self.too_new_user.created_at = timezone.now() - timedelta(days=2)
        self.too_new_user.save()

    def test_valid_positive_reputation(self):
        rep = Reputation(giver=self.giver, receiver=self.receiver, badge="friendly", is_negative=False)
        rep.clean()
        rep.save()

        assert Reputation.objects.count() == 1
        assert Reputation.get_score_for_user(self.receiver) == 1

    def test_valid_negative_reputation(self):
        rep = Reputation(giver=self.giver, receiver=self.receiver, badge="spammy", is_negative=True)
        rep.clean()
        rep.save()

        assert Reputation.get_score_for_user(self.receiver) == -1

    def test_cannot_give_rep_to_self(self):
        rep = Reputation(giver=self.giver, receiver=self.giver, badge="self-love", is_negative=False)
        with pytest.raises(ValidationError, match="You cannot give reputation to yourself."):
            rep.clean()

    def test_cannot_give_rep_if_too_new(self):
        rep = Reputation(giver=self.too_new_user, receiver=self.receiver, badge="too-soon", is_negative=False)
        with pytest.raises(ValidationError, match="You must be registered for at least 7 days"):
            rep.clean()

    def test_unique_constraint(self):
        # First rep is fine
        Reputation.objects.create(giver=self.giver, receiver=self.receiver, badge="unique", is_negative=False)
        # Second from same giver to same receiver should fail
        with pytest.raises(Exception):
            Reputation.objects.create(giver=self.giver, receiver=self.receiver, badge="duplicate", is_negative=True)
