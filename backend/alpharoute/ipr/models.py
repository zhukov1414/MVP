import datetime

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction

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
    progress = models.PositiveIntegerField(default=0,
                                           validators=[MaxValueValidator(100)])

    class Meta:
        verbose_name = 'Индивиуальный план развития'
        verbose_name_plural = 'Планы развития'


class Comment(models.Model):
    author = models.ForeignKey(CustomUser,
                               on_delete=models.CASCADE,
                               related_name='author')
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

    def __str__(self):
        return self.content


class Task(BaseTaskModel):
    ipr = models.ForeignKey(
        IndividualDevelopmentPlan,
        on_delete=models.CASCADE, related_name='task')
    deadline = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=12,
                              choices=StatusTask.choices,
                              default=StatusTask.NOCOMLETED)
    comments = models.ForeignKey(Comment, on_delete=models.CASCADE,
                                 null=True,
                                 blank=True,
                                 related_name='tasks_comments')

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'

    def __str__(self):
        return self.title


@receiver(post_save, sender=IndividualDevelopmentPlan)
def update_progress(sender, instance, created, **kwargs):
    if created:
        return

    with transaction.atomic():
        total_tasks = instance.task.count()
        completed_tasks = instance.task.filter(status=StatusTask.DONE).count()

        if total_tasks > 0:
            progress = (completed_tasks / total_tasks) * 100
        else:
            progress = 0

        if instance.progress != progress:  # Проверяем изменение поля progress
            instance.progress = progress
            instance.save()


@receiver(post_save, sender=Task)
def update_ipr_status(sender, instance, created, **kwargs):
    if created:
        return

    with transaction.atomic():
        if instance.ipr:
            task_status = instance.status
            ipr_status = None

            if task_status == StatusTask.INWORK:
                ipr_status = StatusIpr.INWORK
            elif task_status == StatusTask.DONE:
                ipr_status = StatusIpr.DONE
            else:
                ipr_status = StatusIpr.CREATED

            if instance.ipr.status != ipr_status:  # Проверяем изменение поля
                instance.ipr.status = ipr_status
                instance.ipr.save()

# TODO: при пустой БД ипр и задача создается, прогресс рассчитывается
# НО статус ИПР меняется на самый высокий, если такой есть у одной из задач
