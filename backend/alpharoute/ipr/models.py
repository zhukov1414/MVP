from django.db import models

from employee.models import CustomUser, Employee


class Status(models.Model):
    name = models.CharField('статус',
                            max_length=50,
                            unique=True,)

    class Meta:
        verbose_name = 'Статус'
        verbose_name_plural = 'Статусы'
        ordering = ['id']

    def __str__(self):
        return self.name


class IndividualDevelopmentPlan(models.Model):
    title = models.CharField(max_length=255,)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    goal = models.CharField(max_length=255)
    deadline = models.DateField()
    status = models.ForeignKey(
        Status,
        on_delete=models.CASCADE,
        related_name='ipr',
        verbose_name='статус',
    )

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
    status = models.ForeignKey(
        Status,
        on_delete=models.CASCADE,
        related_name='task',
        verbose_name='статус',
        null=True, blank=True
    )

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'        

    def __str__(self):
        return self.title


class Comment(models.Model):  # добавила автора и задачу
    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='comments')
    task = models.ForeignKey(
        Task, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    postdate = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-postdate']
