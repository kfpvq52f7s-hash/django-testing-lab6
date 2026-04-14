from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, verbose_name='Email')
    phone = models.CharField(max_length=20, blank=True, verbose_name='Номер телефона')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name='Аватар')
    bio = models.TextField(blank=True, verbose_name='О себе')
    friends = models.ManyToManyField('self', blank=True, verbose_name='Друзья')

    def __str__(self):
        return self.username

    def is_friend(self, other_user):
        """Проверяет, является ли other_user другом текущего пользователя"""
        return other_user in self.friends.all()

    def is_friend_with(self, other_user):
        """Проверяет, являются ли пользователи друзьями (взаимно)"""
        return self.is_friend(other_user) or other_user.is_friend(self)