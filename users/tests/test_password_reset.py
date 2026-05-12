import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
class TestPasswordResetFlow:

    @pytest.fixture(autouse=True)
    def prepare(self, client):
        self.client = client
        self.existing_user = User.objects.create_user(
            username='forgetful',
            email='forgetful@mail.ru',
            password='OldPassword99'
        )

    def test_reset_page_loads(self):
        resp = self.client.get(reverse('password_reset'))
        assert resp.status_code == 200

    def test_reset_with_known_email_redirects(self):
        resp = self.client.post(reverse('password_reset'), {
            'email': 'forgetful@mail.ru'
        })
        assert resp.status_code == 302
        assert resp.url == reverse('password_reset_done')

    def test_reset_with_unknown_email_also_redirects(self):
        resp = self.client.post(reverse('password_reset'), {
            'email': 'unknown_person@mail.ru'
        })
        assert resp.status_code == 302
        assert resp.url == reverse('password_reset_done')

    def test_done_page_accessible(self):
        resp = self.client.get(reverse('password_reset_done'))
        assert resp.status_code == 200

    def test_blank_email_rejected(self):
        resp = self.client.post(reverse('password_reset'), {
            'email': ''
        })
        assert resp.status_code == 200
        assert 'email' in resp.context['form'].errors
