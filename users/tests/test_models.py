import pytest
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
class TestCustomUserDatabase:

    def test_create_regular_user(self):
        new_user = User.objects.create_user(
            username='student_max',
            email='max@corp.ru',
            password='MaxSecret1!',
            phone='+79035552211'
        )
        assert new_user.pk is not None
        assert new_user.username == 'student_max'
        assert new_user.email == 'max@corp.ru'
        assert new_user.phone == '+79035552211'
        assert new_user.check_password('MaxSecret1!')
        assert new_user.is_active is True
        assert new_user.is_staff is False
        assert new_user.is_superuser is False

    def test_create_admin_user(self):
        superuser = User.objects.create_superuser(
            username='chief',
            email='chief@corp.ru',
            password='AdminUltra#1'
        )
        assert superuser.is_superuser is True
        assert superuser.is_staff is True

    def test_user_string_is_username(self):
        user = User.objects.create_user(
            username='ironman',
            email='stark@avengers.ru',
            password='Jarvis#1'
        )
        assert str(user) == 'ironman'

    def test_email_case_preserved(self):
        user = User.objects.create_user(
            username='mixedcase',
            email='Mixed.CASE@Example.RU',
            password='Case12345'
        )
        assert user.email == 'Mixed.CASE@Example.RU'

    @pytest.mark.parametrize('login,email_addr,phone_num', [
        ('volunteer1', 'vol1@ngo.org', '+79160001122'),
        ('volunteer2', 'vol2@ngo.org', '+79160003344'),
        ('volunteer3', 'vol3@ngo.org', '+79160005566'),
        ('volunteer4', 'vol4@ngo.org', '+79160007788'),
    ])
    def test_batch_user_creation(self, login, email_addr, phone_num):
        u = User.objects.create_user(
            username=login,
            email=email_addr,
            password='Volunteer#Pass',
            phone=phone_num
        )
        assert u.username == login
        assert u.email == email_addr
        assert u.phone == phone_num
