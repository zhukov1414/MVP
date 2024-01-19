from django.db import models
from django.utils.translation import gettext_lazy as _

import datetime

from employee.models import CustomUser as Employee


STATUS = [
        (0, 'Выполнен'),
        (1, 'Не выполнен'),
        (2, 'В работе'),
        (3, 'Отсутствует'),
        (4, 'Отменен'),
    ]


class BaseTaskModel(models.Model):
    """Абстрактная модель для задач и шаблонов"""

    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    linkURL = models.CharField(max_length=255,
                               null=True, blank=True)

    class Meta:
        abstract = True


class Task(BaseTaskModel):
    deadline = models.DateField(null=True, blank=True)
    status = models.PositiveSmallIntegerField(_('status'), choices=STATUS)

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'

    def __str__(self):
        return self.title


class Comment(models.Model):
    author = models.ForeignKey(
        Employee, on_delete=models.CASCADE, related_name='comments')
    task = models.ForeignKey(
        Task, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    postdate = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-postdate']

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.postdate = datetime.datetime.now()
        super().save(*args, **kwargs)


class IndividualDevelopmentPlan(models.Model):
    """Модель индивидуального плана развития"""

    title = models.CharField(max_length=255,
                             verbose_name = 'Название ИПР',)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE,
                                 verbose_name = 'Сотрудник',)
    goal = models.CharField(max_length=255,
                            verbose_name = 'Цель',)
    description = models.TextField(verbose_name = 'Описание',)
    deadline = models.DateField(verbose_name = 'Дата',)
    task = models.ManyToManyField(Task,
                                  related_name = 'task',
                                  verbose_name='Задачи')

    class Meta:
        verbose_name = 'Индивиуальный план развития'
        verbose_name_plural = 'Планы развития'

    def __str__(self):
        return f'{self.title} - {self.employee}'