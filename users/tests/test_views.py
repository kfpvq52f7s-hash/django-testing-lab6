import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.test import Client

User = get_user_model()


@pytest.mark.django_db
class TestAuthViews:

    def setup_method(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

    def test_register_view_get(self):
        response = self.client.get(reverse('register'))
        assert response.status_code == 200
        # Исправлено: ожидаем 'users/register.html'
        assert 'users/register.html' in response.template_name

    def test_register_view_post_success(self):
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'email': 'new@example.com',
            'phone': '+79991112233',
            'password1': 'strongpass123',
            'password2': 'strongpass123'
        })
        assert response.status_code in [302, 200]

    def test_login_view_get(self):
        response = self.client.get(reverse('login'))
        assert response.status_code == 200
        # Исправлено: ожидаем 'registration/login.html'
        assert 'registration/login.html' in response.template_name

    def test_login_view_post_success(self):
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpass123'
        })
        assert response.status_code == 302
        assert response.url == '/'

    def test_login_view_post_invalid(self):
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        assert response.status_code == 200
        # Исправлено: ожидаем 'registration/login.html'
        assert 'registration/login.html' in response.template_name

    def test_logout_view(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('logout'))
        assert response.status_code == 302
        assert response.url == '/'

    def test_home_page_authenticated(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('home'))
        assert response.status_code == 200
        assert 'testuser' in response.content.decode()

    def test_home_page_anonymous(self):
        response = self.client.get(reverse('home'))
        assert response.status_code == 200
        content = response.content.decode()
        assert 'Войти' in content or 'Login' in content