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


class Department1(models.TextChoices):
    """Департаменты."""

    ART = 'art', _('Дизайн')
    QA = 'QA', _('QA')
    BA = 'BA', _('BA')
    SA = 'SA', _('SA')


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

    title = models.CharField('Название', max_length=255)
    description = models.TextField('Описание', null=True, blank=True)
    linkURL = models.CharField('Ссылка', max_length=255,
                               null=True, blank=True)

    class Meta:
        abstract = True


class IndividualDevelopmentPlan(models.Model):

    title = models.CharField('Название', max_length=255,)
    employee = models.ForeignKey(CustomUser, on_delete=models.CASCADE,
                                 related_name='ipr_employee',
                                 verbose_name='Сотрудник',)
    goal = models.CharField('Цель', max_length=255)
    description = models.TextField('Описание')
    deadline = models.DateField('Дедлайн')
    status = models.CharField('Статус', max_length=12,
                              choices=StatusIpr.choices,
                              default=StatusIpr.CREATED)

    class Meta:
        verbose_name = 'Индивиуальный план развития'
        verbose_name_plural = 'Планы развития'

    def __str__(self):
        return self.title


class Task(BaseTaskModel):
    ipr = models.ForeignKey(
        IndividualDevelopmentPlan,
        on_delete=models.CASCADE, related_name='task',
        verbose_name='ИПР')
    deadline = models.DateField('Дедлайн', null=True, blank=True)
    status = models.CharField('Статус', max_length=12,
                              choices=StatusTask.choices,
                              default=StatusTask.NOCOMLETED)

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'

    def __str__(self):
        return self.title


class Comment(models.Model):
    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='comments',
        verbose_name='Автор')
    task = models.ForeignKey(
        Task, on_delete=models.CASCADE, related_name='comments',
        verbose_name='Задача')
    content = models.TextField('Текст комментария')
    postdate = models.DateTimeField('Дата создания',
                                    auto_now_add=True, db_index=True)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-postdate']

    def save(self, *args, **kwargs):
        self.postdate = datetime.datetime.now()
        super().save(*args, **kwargs)


class Template(BaseTaskModel):
    department = models.CharField('Департамент', max_length=12,
                                  choices=Department1.choices)

    class Meta:
        verbose_name = 'Шаблон'
        verbose_name_plural = 'Шаблоны'
        ordering = ['department']

    def __str__(self):
        return str(self.department)
