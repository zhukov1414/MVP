from django.db import models
from django.utils.translation import gettext_lazy as _

from ipr.models import BaseTaskModel


class Department(models.Model):

    DEPARTMENT = [
        (0, 'Дизайн'),
        (1, 'QA'),
        (2, 'BA'),
        (3, 'SA'),
    ]

    title = models.PositiveSmallIntegerField(_('title'), choices=DEPARTMENT)

    class Meta:
        verbose_name = 'направление'
        verbose_name_plural = 'направления'
        ordering = ['title']

    def __str__(self):
        return str(self.title)


class Template(BaseTaskModel):
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Шаблон'
        verbose_name_plural = 'Шаблоны'
        ordering = ['department']

    def __str__(self):
        return str(self.department)
