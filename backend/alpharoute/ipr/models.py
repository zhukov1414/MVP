from django.db import models

from employee.models import EmployeeCustomUser as Employee


class Comment(models.Model):
    # id = models.CharField(max_length=255, primary_key=True)
    # это поле автоматически присваиватеся, оно точно нужно?
    author = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        verbose_name='Автор')
    content = models.TextField()
    postdate = models.DateField()

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'


class Task(models.Model):
    # id = models.CharField(max_length=255, primary_key=True)
    title = models.CharField(max_length=255)
    deadline = models.DateField()
    description = models.TextField()
    status = models.CharField(max_length=50)
    linkURL = models.CharField(max_length=255)
    comments = models.ManyToManyField(
        Comment,
        verbose_name='Комментарии'
        )

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'


class IndividualDevelopmentPlan(models.Model):
    # id = models.CharField(max_length=255, primary_key=True)
    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        verbose_name='Сотрудник',
        )
    goal = models.CharField(max_length=255)
    deadline = models.DateField()
    status = models.CharField(max_length=50)
    tasks = models.ManyToManyField(
        Task,
        verbose_name='Задачи',
        )

    class Meta:
        verbose_name = 'Индивидуальный план'
        verbose_name_plural = 'Индивидуальный план'
        ordering = ['id']
