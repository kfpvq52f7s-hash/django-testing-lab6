from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.core.mail import send_mail
from django.conf import settings
from .models import CustomUser


# Форма регистрации
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email')
    phone = forms.CharField(required=False, max_length=20, label='Номер телефона')

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'phone', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Имя пользователя'
        self.fields['password1'].label = 'Пароль'
        self.fields['password2'].label = 'Подтверждение пароля'


# Форма восстановления пароля
class CustomPasswordResetForm(PasswordResetForm):
    def send_mail(self, subject_template_name, email_template_name,
                  context, from_email, to_email, html_email_template_name=None):
        user = context.get('user')
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        reset_link = f"{settings.BASE_URL}/auth/reset/{uid}/{token}/"

        # English email message
        email_subject = "Password Reset"
        email_message = f"""
Hello!

You received this email because you requested a password reset on the website.

To reset your password, click the link below:
{reset_link}

If you did not request a password reset, please ignore this email.

Best regards,
Site Administrator
"""

        send_mail(
            subject=email_subject,
            message=email_message,
            from_email=from_email,
            recipient_list=[to_email],
            fail_silently=False,
        )