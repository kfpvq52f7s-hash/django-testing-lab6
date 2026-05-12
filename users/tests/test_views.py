import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
class TestAuthAndViews:

    @pytest.fixture(autouse=True)
    def prepare(self, client):
        self.client = client
        self.regular_user = User.objects.create_user(
            username='sergey',
            email='sergey@lab.ru',
            password='SergeyPass1'
        )

    def test_register_page_get(self):
        resp = self.client.get(reverse('register'))
        assert resp.status_code == 200
        assert 'users/register.html' in resp.template_name

    def test_register_new_user_success(self):
        resp = self.client.post(reverse('register'), {
            'username': 'fresher',
            'email': 'fresh@lab.ru',
            'phone': '+79269876543',
            'password1': 'Fresh#2024',
            'password2': 'Fresh#2024'
        })
        assert resp.status_code in [302, 200]

    def test_login_page_get(self):
        resp = self.client.get(reverse('login'))
        assert resp.status_code == 200
        assert 'registration/login.html' in resp.template_name

    def test_login_correct_credentials(self):
        resp = self.client.post(reverse('login'), {
            'username': 'sergey',
            'password': 'SergeyPass1'
        })
        assert resp.status_code == 302
        assert resp.url == '/'

    def test_login_wrong_password(self):
        resp = self.client.post(reverse('login'), {
            'username': 'sergey',
            'password': 'wrong_one'
        })
        assert resp.status_code == 200
        assert 'registration/login.html' in resp.template_name

    def test_logout_redirects_home(self):
        self.client.login(username='sergey', password='SergeyPass1')
        resp = self.client.post(reverse('logout'))
        assert resp.status_code == 302
        assert resp.url == '/'

    def test_home_shows_username_when_authenticated(self):
        self.client.login(username='sergey', password='SergeyPass1')
        resp = self.client.get(reverse('home'))
        assert resp.status_code == 200
        assert 'sergey' in resp.content.decode()

    def test_home_shows_login_for_anonymous(self):
        resp = self.client.get(reverse('home'))
        assert resp.status_code == 200
        content = resp.content.decode()
        assert 'Login' in content or 'Войти' in content
