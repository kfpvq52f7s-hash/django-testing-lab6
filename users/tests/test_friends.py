import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.test import Client

User = get_user_model()


@pytest.mark.django_db
class TestFriendsFeature:

    def setup_method(self):
        self.client = Client()
        self.user1 = User.objects.create_user(
            username='user1',
            email='user1@test.com',  # Добавлен email
            password='pass123'
        )
        self.user2 = User.objects.create_user(
            username='user2',
            email='user2@test.com',  # Добавлен email
            password='pass123'
        )

    def test_add_friend(self):
        self.client.login(username='user1', password='pass123')
        response = self.client.post(reverse('add_friend', kwargs={'username': 'user2'}))
        assert response.status_code == 302
        assert self.user2 in self.user1.friends.all()

    def test_remove_friend(self):
        self.user1.friends.add(self.user2)
        self.client.login(username='user1', password='pass123')
        response = self.client.post(reverse('remove_friend', kwargs={'username': 'user2'}))
        assert response.status_code == 302
        assert self.user2 not in self.user1.friends.all()