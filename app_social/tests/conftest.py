import pytest
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.fixture
def user1(db):
    user = User.objects.create_user(
        email="user1@example.com",
        username="user1",
        mc_username="user1_mc",
        password="pass123"
    )
    user.created_at = timezone.now() - timedelta(days=10)
    user.save()
    return user


@pytest.fixture
def user2(db):
    user = User.objects.create_user(
        email="user2@example.com",
        username="user2",
        mc_username="user2_mc",
        password="pass123"
    )
    user.created_at = timezone.now() - timedelta(days=10)
    user.save()
    return user
