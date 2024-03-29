from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


class CustomUser(AbstractUser):
    """Модель пользователя."""
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['name', 'position',]

    username = models.CharField(
        max_length=150,
        unique=True,
        verbose_name='Логин',
        validators=([RegexValidator(
            regex=r'^(?!me$).*$',
            message='Неподходящий логин. "me" использовать запрещено.')]))
    name = models.CharField('Имя сотрудника', max_length=150)
    position = models.CharField('Должность', max_length=150)
    password = models.CharField('Пароль', max_length=150)
    manager = models.ForeignKey(  # для тех, у кого есть руководитель
        "CustomUser", on_delete=models.SET_NULL,
        verbose_name="manager",
        related_name="employee",
        blank=True, null=True,)
    photo = models.ImageField('Фото', upload_to='photo',
                              blank=True, null=True,)

    class Meta:
        verbose_name = 'Пользователь',
        verbose_name_plural = 'Пользователи'
        ordering = ['id']

    def __str__(self):
        return f'{self.name} - {self.position}'
