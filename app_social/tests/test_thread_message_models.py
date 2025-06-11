import pytest
from django.contrib.auth import get_user_model
from app_social.models import Thread, Message

User = get_user_model()


@pytest.mark.django_db
def test_thread_creation_between_two_users(user1, user2):
    thread = Thread.get_or_create_between(user1, user2)

    assert thread.user1 in [user1, user2]
    assert thread.user2 in [user1, user2]
    assert thread.user1 != thread.user2
    assert Thread.objects.count() == 1


@pytest.mark.django_db
def test_message_creation_updates_thread_timestamp(user1, user2):
    thread = Thread.get_or_create_between(user1, user2)
    initial_updated_at = thread.updated_at

    message = Message.objects.create(thread=thread, sender=user1, content="Hello!")

    thread.refresh_from_db()
    assert message in thread.messages.all()
    assert thread.updated_at > initial_updated_at


@pytest.mark.django_db
def test_cannot_create_thread_with_self(user1):
    with pytest.raises(Exception):
        thread = Thread(user1=user1, user2=user1)
        thread.clean()
        thread.save()
