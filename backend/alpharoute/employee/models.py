from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    name = models.CharField('Имя', max_length=150)
    first_name = models.CharField('Отчество', max_length=150)
    last_name = models.CharField('Фамилия', max_length=150)
    position = models.CharField(max_length=150)
    password = models.CharField(max_length=150)
    manager = models.ForeignKey(  # для тех, у кого есть руководитель
        "CustomUser", on_delete=models.SET_NULL,
        verbose_name="manager",
        related_name="employee",
        blank=True, null=True,)
    image = models.ImageField(  # как оказалось, он нам нужен
        'Аватар',
        upload_to='static/recipe/',
        blank=True,
        null=True)

    class Meta:
        verbose_name = 'сотрудник',
        verbose_name_plural = 'Сотрудники'
        ordering = ['id']

    def __str__(self):
        return f'{self.name} - {self.position}'
