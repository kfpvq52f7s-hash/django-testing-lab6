import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.test import Client

User = get_user_model()


@pytest.mark.django_db
class TestPermissions:

    def setup_method(self):
        self.client = Client()
        self.user1 = User.objects.create_user(
            username='user1',
            email='user1@test.com',
            password='pass123'
        )
        self.user2 = User.objects.create_user(
            username='user2',
            email='user2@test.com',
            password='pass123'
        )

    def test_profile_access_for_owner(self):
        self.client.login(username='user1', password='pass123')
        response = self.client.get(reverse('profile', kwargs={'username': 'user1'}))
        assert response.status_code == 200

    def test_edit_profile_only_for_owner(self):
        self.client.login(username='user1', password='pass123')
        response = self.client.get(reverse('edit_profile'))
        assert response.status_code == 200

    def test_unauthorized_cannot_edit_profile(self):
        response = self.client.get(reverse('edit_profile'))
        assert response.status_code == 302
        assert response.url.startswith('/auth/login/')

    def test_unauthorized_cannot_view_user_list(self):
        response = self.client.get(reverse('user_list'))
        assert response.status_code == 302
        assert response.url.startswith('/auth/login/')

    def test_authenticated_can_view_user_list(self):
        self.client.login(username='user1', password='pass123')
        response = self.client.get(reverse('user_list'))
        assert response.status_code == 200