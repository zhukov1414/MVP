import datetime

from django.db import models
from django.utils.translation import gettext_lazy as _

from users.models import CustomUser


class StatusIpr(models.TextChoices):
    """Статусы для индивидуального плана развития."""

    CREATED = 'created', _('Создан')
    INWORK = 'inwork', _('В работе')
    DONE = 'done', _('Выполнен')
    CHECKED = 'checked', _('Проверен')
    STOPED = 'stoped', _('Приостановлен')


class StatusTask(models.TextChoices):
    """Статусы для задач в ИПР."""

    NOCOMLETED = 'nocompleted', _('Не выполнено')
    INWORK = 'inwork', _('В работе')
    DONE = 'done', _('Выполнен')


class PubDateModel(models.Model):
    """Абстрактная модель для времени."""

    pub_date = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
        db_index=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.pub_date


class BaseTaskModel(models.Model):
    """Абстрактная модель для задач и шаблонов."""

    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    linkURL = models.CharField(max_length=255,
                               null=True, blank=True)

    class Meta:
        abstract = True


class IndividualDevelopmentPlan(models.Model):
    title = models.CharField(max_length=255,)
    employee = models.ForeignKey(CustomUser, on_delete=models.CASCADE,
                                 related_name='ipr_employee',
                                 verbose_name='сотрудник',)
    goal = models.CharField(max_length=255)
    description = models.TextField()
    deadline = models.DateField()
    status = models.CharField(max_length=12,
                              choices=StatusIpr.choices,
                              default=StatusIpr.CREATED)

    class Meta:
        verbose_name = 'Индивиуальный план развития'
        verbose_name_plural = 'Планы развития'

    def __str__(self):
        return self.title


class Comment(models.Model):
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


class Task(BaseTaskModel):
    ipr = models.ForeignKey(
        IndividualDevelopmentPlan,
        on_delete=models.CASCADE, related_name='task')
    deadline = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=12,
                              choices=StatusTask.choices,
                              default=StatusTask.NOCOMLETED)
    comments = models.ForeignKey(Comment, on_delete=models.CASCADE,
                                 related_name='tasks_comments')

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'

    def __str__(self):
        return self.title
