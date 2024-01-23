import datetime

from django.db import models
from django.utils.translation import gettext_lazy as _

from employee.models import CustomUser
from ipr.constants import STATUS_IPR, STATUS_TASK


class PubDateModel(models.Model):
    """Абстрактная модель для времени"""

    pub_date = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
        db_index=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.pub_date


class IndividualDevelopmentPlan(PubDateModel):

    title = models.CharField(max_length=255,)
    # author = models.ForeignKey(  # хочу, чтобы был
    #     CustomUser,
    #     on_delete=models.CASCADE,
    #     related_name='ipr_author',
    #     verbose_name='автор',
    # )
    employee = models.ForeignKey(CustomUser, on_delete=models.CASCADE,
                                 related_name='ipr_employee',
                                 verbose_name='сотрудник',)
    goal = models.CharField(max_length=255)
    description = models.TextField()
    deadline = models.DateField()
    status = models.PositiveSmallIntegerField(_('status'), choices=STATUS_IPR,
                                              default=0,)

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


class Task(BaseTaskModel,PubDateModel):
    ipr = models.ForeignKey(
        IndividualDevelopmentPlan,
        on_delete=models.CASCADE, related_name='task',
        verbose_name="ipr")
    deadline = models.DateField(null=True, blank=True)
    status = models.PositiveSmallIntegerField(_('status'), choices=STATUS_TASK)

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'

    def __str__(self):
        return self.title


class Comment(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE,
                               related_name='comments')
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
