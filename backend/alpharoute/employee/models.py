from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

MAX_CHAR_LENGTH = 150


class CustomUser(AbstractUser):  # предлагаю его все-таки переопределить,

    REQUIRED_FIELDS = ['first_name', 'last_name',]
    USER = 'user'
    MANAGER = 'manager'
    ADMIN = 'admin'

    USER_ROLES = (
        (USER, 'user'),
        (MANAGER, 'manager'),
        (ADMIN, 'admin'),
    )

    username = models.CharField(
        max_length=MAX_CHAR_LENGTH,
        unique=True,
        verbose_name='Логин',
        validators=([RegexValidator(
            regex=r'^(?!me$).*$',
            message='Неподходящий логин. "me" использовать запрещено.')]))
    email = models.EmailField(
        max_length=254,
        unique=True,
        verbose_name='Электронная почта',)
    first_name = models.CharField(max_length=MAX_CHAR_LENGTH,
                                  verbose_name='Имя',
                                  blank=True)
    last_name = models.CharField(max_length=MAX_CHAR_LENGTH,
                                 verbose_name='Фамилия',
                                 blank=True)
    role = models.CharField(max_length=MAX_CHAR_LENGTH,
                            verbose_name='Роль',
                            choices=USER_ROLES,
                            default=USER)

    class Meta:
        verbose_name = 'Пользователь',
        verbose_name_plural = 'Пользователи'
        ordering = ['id']

    @property
    def is_user(self):
        return self.role == self.USER

    @property
    def is_manager(self):
        return self.role == self.MANAGER

    @property
    def is_admin(self):
        return self.role == self.ADMIN

    def __str__(self):
        return self.username


class Employee(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='employee',
        verbose_name='сотрудник',)
    position = models.CharField(max_length=MAX_CHAR_LENGTH)

    class Meta:
        unique_together = ['user', 'position']
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'

    def __str__(self):
        return f'{self.user} - {self.position} '
