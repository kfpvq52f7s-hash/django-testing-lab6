import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
class TestAccessControl:

    @pytest.fixture(autouse=True)
    def prepare_users(self, client):
        self.client = client
        self.owner = User.objects.create_user(
            username='django_dev',
            email='dev@team.ru',
            password='CodeMaster42'
        )
        self.outsider = User.objects.create_user(
            username='random_guy',
            email='random@team.ru',
            password='Random#11'
        )

    def test_owner_sees_own_profile(self):
        self.client.login(username='django_dev', password='CodeMaster42')
        resp = self.client.get(reverse('profile', kwargs={'username': 'django_dev'}))
        assert resp.status_code == 200

    def test_authenticated_sees_edit_page(self):
        self.client.login(username='django_dev', password='CodeMaster42')
        resp = self.client.get(reverse('edit_profile'))
        assert resp.status_code == 200

    def test_guest_redirected_from_edit(self):
        resp = self.client.get(reverse('edit_profile'))
        assert resp.status_code == 302
        assert '/auth/login/' in resp.url

    def test_guest_redirected_from_user_list(self):
        resp = self.client.get(reverse('user_list'))
        assert resp.status_code == 302
        assert '/auth/login/' in resp.url

    def test_logged_in_user_sees_list(self):
        self.client.login(username='django_dev', password='CodeMaster42')
        resp = self.client.get(reverse('user_list'))
        assert resp.status_code == 200
