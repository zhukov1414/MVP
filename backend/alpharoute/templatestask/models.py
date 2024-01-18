from django.db import models

from ipr.models import BaseTaskModel


class Department(models.Model):
    title = models.CharField(max_length=255,)

    class Meta:
        verbose_name = 'отдел/направление'
        verbose_name_plural = 'отдел/направление'
        ordering = ['title']

    def __str__(self):
        return self.title


class Template(BaseTaskModel):
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Шаблон'
        verbose_name_plural = 'Шаблоны'
        ordering = ['department']

    def __str__(self):
        return f'{self.department} - {self.title}'
