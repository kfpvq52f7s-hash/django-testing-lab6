import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
class TestFriendSystem:

    @pytest.fixture(autouse=True)
    def prepare_users(self, client):
        self.client = client
        self.alice = User.objects.create_user(
            username='alice',
            email='alice@friends.ru',
            password='Wonderland1'
        )
        self.bob = User.objects.create_user(
            username='bob',
            email='bob@friends.ru',
            password='Builder#2'
        )

    def test_send_friend_request_works(self):
        self.client.login(username='alice', password='Wonderland1')
        url = reverse('add_friend', kwargs={'username': 'bob'})
        resp = self.client.post(url)
        assert resp.status_code == 302
        assert self.bob in self.alice.friends.all()

    def test_remove_friend_works(self):
        self.alice.friends.add(self.bob)
        self.client.login(username='alice', password='Wonderland1')
        url = reverse('remove_friend', kwargs={'username': 'bob'})
        resp = self.client.post(url)
        assert resp.status_code == 302
        assert self.bob not in self.alice.friends.all()

    def test_cannot_add_already_friend(self):
        self.alice.friends.add(self.bob)
        self.client.login(username='alice', password='Wonderland1')
        url = reverse('add_friend', kwargs={'username': 'bob'})
        self.client.post(url)
        assert self.alice.friends.filter(pk=self.bob.pk).count() == 1

    def test_guest_cannot_add_friend(self):
        url = reverse('add_friend', kwargs={'username': 'bob'})
        resp = self.client.post(url)
        assert resp.status_code == 302
        assert '/auth/login/' in resp.url
