from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


class CustomUser(AbstractUser):
    """Модель пользователя."""
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    username = models.CharField(
        max_length=150,
        unique=True,
        verbose_name='Логин',
        validators=([RegexValidator(
            regex=r'^(?!me$).*$',
            message='Неподходящий логин. "me" использовать запрещено.')]))
    name = models.CharField('Имя', max_length=150)
    first_name = models.CharField('Отчество', max_length=150)
    last_name = models.CharField('Фамилия', max_length=150)
    position = models.CharField(max_length=150)
    password = models.CharField(max_length=150)
    photo = models.ImageField('Фото', upload_to='photo',
                              blank=True, null=True,)

    class Meta:
        verbose_name = 'Пользователь',
        verbose_name_plural = 'Пользователи'
        ordering = ['id']

    def __str__(self):
        return f'{self.name} - {self.position}'
