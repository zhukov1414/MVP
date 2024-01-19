from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):

    position = models.CharField(max_length=150)
    password = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'сотрудник',
        verbose_name_plural = 'Сотрудники'
        ordering = ['id']

    def __str__(self):
        return f'{self.username} - {self.position}'
