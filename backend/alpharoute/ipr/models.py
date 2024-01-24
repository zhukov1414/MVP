import datetime

from django.db import models
from django.utils.translation import gettext_lazy as _

from employee.models import CustomUser
#from ipr.constants import STATUS_IPR, STATUS_TASK


class StatusIpr(models.TextChoices):
    CREATED = 'created', _('Создан')
    INWORK = 'inwork', _('В работе')
    DONE = 'done', _('Выполнен')
    CHECKED = 'checked', _('Проверен')
    STOPED = 'stoped', _('Приостановлен')

class StatusTask(models.TextChoices):
    NOCOMLETED = 'nocompleted', _('Не выполнено')
    INWORK = 'inwork', _('В работе')
    DONE = 'done', _('Выполнен')


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


class BaseTaskModel(models.Model):
    """Абстрактная модель для задач и шаблонов"""
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    linkURL = models.CharField(max_length=255,
                               null=True, blank=True)

    class Meta:
        abstract = True


class Task(BaseTaskModel,PubDateModel):

    deadline = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=12,
                              choices=StatusTask.choices,
                              default=StatusTask.NOCOMLETED)

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'

    def __str__(self):
        return self.title


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
    status = models.CharField(max_length=12,
                              choices=StatusIpr.choices,
                              default=StatusIpr.CREATED)
    task = models.ManyToManyField(Task,
                                  related_name = 'task',
                                  verbose_name='Задачи')
    
    """ИПР создан, статус меняется на Создан"""
    def is_created(self):
        return self.status == StatusIpr.CREATED

    """Хотя бы одна Задача Task В работе, статус меняется на В работе"""
    def is_inwork(self):
        return self.status == self.task.filter(status=StatusTask.INWORK).exists()

    """Все Задачи Task Выполнены, статус меняется на Выполнен"""
    def is_done(self, task):
        for task.status in StatusTask:
            if task.status != StatusTask.DONE:
                return StatusIpr.INWORK
        return StatusIpr.DONE

    """Все задачи Task Выполнены, статус меняется на Проверен, изменять может только Руководитель """
    def is_checked(self):
        return self.status == StatusIpr.CHECKED

    """Изменять может только Руководитель, поставлена на паузу, статус Отменен """
    def is_stoped(self):
        return self.status == StatusIpr.STOPED


    class Meta:
        verbose_name = 'Индивиуальный план развития'
        verbose_name_plural = 'Планы развития'

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
