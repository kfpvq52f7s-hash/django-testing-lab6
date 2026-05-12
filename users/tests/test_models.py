import pytest
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
class TestUserModel:

    def test_create_user(self):
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            phone='+79991234567'
        )
        assert user.username == 'testuser'
        assert user.email == 'test@example.com'
        assert user.phone == '+79991234567'
        assert user.check_password('testpass123')

    def test_create_superuser(self):
        admin = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpass123'
        )
        assert admin.is_superuser
        assert admin.is_staff

    def test_user_str_method(self):
        user = User.objects.create_user(username='testuser', password='pass')
        assert str(user) == 'testuser'

    @pytest.mark.parametrize('username,email,password', [
        ('user_a', 'a@test.com', 'pass123'),
        ('user_b', 'b@test.com', 'pass456'),
        ('user_c', 'c@test.com', 'pass789'),
    ])
    def test_multiple_users_creation(self, username, email, password):
        user = User.objects.create_user(username=username, email=email, password=password)
        assert user.username == username
        assert user.email == email
