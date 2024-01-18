from django.contrib.auth.models import AbstractUser
from django.db import models

MAX_CHAR_LENGTH = 150


class EmployeeCustomUser(AbstractUser):
    USER = 'user'
    MANAGER = 'manager'
    ADMIN = 'admin'

    USER_ROLES = (
        (USER, 'user'),
        (MANAGER, 'manager'),
        (ADMIN, 'admin'),
    )

    username = models.CharField(
        'Логин',
        max_length=150,
        blank=False,
        null=False,
        unique=True)
    first_name = models.CharField(
        'Имя',
        max_length=150,
        blank=False,
        null=False,)
    last_name = models.CharField(
        'Фамилия',
        max_length=150,
        blank=False,
        null=False,)
    password = models.CharField(
        'Пароль',
        max_length=150,
        blank=False,
        null=False,)
    position = models.CharField(
        'Должность',
        max_length=255,
        blank=False,
        null=False,)
    role = models.CharField(
        'Роль',
        max_length=MAX_CHAR_LENGTH,
        choices=USER_ROLES,
        default=USER)

    class Meta:
        verbose_name = 'сотрудник'
        verbose_name_plural = 'Сотрудники'

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
