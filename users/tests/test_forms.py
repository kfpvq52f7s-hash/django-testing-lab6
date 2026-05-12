import pytest
from users.forms import CustomUserCreationForm


@pytest.mark.django_db
class TestSignupFormValidation:

    def test_all_fields_filled_correctly(self):
        """Форма валидна при корректном заполнении всех полей"""
        data = {
            'username': 'alex_student',
            'email': 'alex@university.ru',
            'phone': '+79261234567',
            'password1': 'Secret#2024!',
            'password2': 'Secret#2024!'
        }
        form = CustomUserCreationForm(data=data)
        assert form.is_valid()
        assert form.cleaned_data['username'] == 'alex_student'
        assert form.cleaned_data['email'] == 'alex@university.ru'

    def test_passwords_dont_match(self):
        """Ошибка когда пароли не совпадают"""
        data = {
            'username': 'test_bot',
            'email': 'bot@test.ru',
            'password1': 'AlphaBeta123',
            'password2': 'AlphaBeta999'
        }
        form = CustomUserCreationForm(data=data)
        assert form.is_valid() is False
        assert 'password2' in form.errors
        assert 'совпадают' in str(form.errors['password2']).lower() or 'match' in str(form.errors['password2']).lower()

    def test_email_field_is_required(self):
        """Поле email обязательно"""
        data = {
            'username': 'no_email',
            'password1': 'TestPass#1',
            'password2': 'TestPass#1'
        }
        form = CustomUserCreationForm(data=data)
        assert form.is_valid() is False
        assert 'email' in form.errors

    def test_phone_field_optional(self):
        """Телефон — необязательное поле"""
        data = {
            'username': 'phone_less',
            'email': 'nophone@test.ru',
            'password1': 'NoPhone#1',
            'password2': 'NoPhone#1'
        }
        form = CustomUserCreationForm(data=data)
        assert form.is_valid()

    def test_short_password_rejected(self):
        """Слишком короткий пароль не принимается"""
        data = {
            'username': 'weak_user',
            'email': 'weak@test.ru',
            'password1': '123',
            'password2': '123'
        }
        form = CustomUserCreationForm(data=data)
        assert form.is_valid() is False