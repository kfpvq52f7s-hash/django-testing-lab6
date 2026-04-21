import pytest
from users.forms import CustomUserCreationForm


@pytest.mark.django_db
class TestRegistrationForm:

    def test_valid_registration_form(self):
        form_data = {
            'username': 'newuser',
            'email': 'new@example.com',
            'phone': '+79991112233',
            'password1': 'strongpass123',
            'password2': 'strongpass123'
        }
        form = CustomUserCreationForm(data=form_data)
        assert form.is_valid()

    def test_invalid_registration_form_passwords_mismatch(self):
        form_data = {
            'username': 'newuser',
            'email': 'new@example.com',
            'password1': 'pass123',
            'password2': 'pass456'
        }
        form = CustomUserCreationForm(data=form_data)
        assert not form.is_valid()
        assert 'password2' in form.errors

    def test_invalid_registration_form_missing_email(self):
        form_data = {
            'username': 'newuser',
            'password1': 'pass123',
            'password2': 'pass123'
        }
        form = CustomUserCreationForm(data=form_data)
        assert not form.is_valid()
        assert 'email' in form.errors