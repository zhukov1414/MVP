import datetime

from django.db import models
from django.utils.translation import gettext_lazy as _

from employee.models import CustomUser as Employee

STATUS = [
        (0, 'не выполнен'),
        (1, 'в работе'),
        (2, 'выполнен'),
        (3, 'проверен'),
        (4, 'отменен'),
    ]


class IndividualDevelopmentPlan(models.Model):

    title = models.CharField(max_length=255,)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    goal = models.CharField(max_length=255)
    deadline = models.DateField()
    status = models.PositiveSmallIntegerField(_('status'), choices=STATUS)

    class Meta:
        verbose_name = 'Индивиуальный план развития'
        verbose_name_plural = 'Планы развития'

    def __str__(self):
        return self.title


class BaseTaskModel(models.Model):
    """Абстрактная модель для задач и шаблонов"""
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    linkURL = models.CharField(max_length=255,
                               null=True, blank=True)

    class Meta:
        abstract = True


class Task(BaseTaskModel):
    ipr = models.ForeignKey(
        IndividualDevelopmentPlan,
        on_delete=models.CASCADE, related_name='task')
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
