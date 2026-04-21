import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.test import Client

User = get_user_model()

@pytest.mark.django_db
class TestPasswordReset:
    
    def setup_method(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='oldpass123'
        )
    
    def test_password_reset_form_get(self):
        response = self.client.get(reverse('password_reset'))
        assert response.status_code == 200
    
    def test_password_reset_post_valid_email(self):
        response = self.client.post(reverse('password_reset'), {
            'email': 'test@example.com'
        })
        assert response.status_code == 302
        assert response.url == reverse('password_reset_done')
    
    def test_password_reset_post_invalid_email(self):
        response = self.client.post(reverse('password_reset'), {
            'email': 'nonexistent@example.com'
        })
        assert response.status_code == 302
        assert response.url == reverse('password_reset_done')
    
    def test_password_reset_done_page(self):
        response = self.client.get(reverse('password_reset_done'))
        assert response.status_code == 200
