from django.db import models

from employee.models import Employee


class Comment(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    content = models.TextField()
    postdate = models.DateField()


class Task(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    title = models.CharField(max_length=255)
    deadline = models.DateField()
    description = models.TextField()
    status = models.CharField(max_length=50)
    linkURL = models.CharField(max_length=255)
    comments = models.ManyToManyField(Comment)


class IndividualDevelopmentPlan(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    goal = models.CharField(max_length=255)
    deadline = models.DateField()
    status = models.CharField(max_length=50)
    tasks = models.ManyToManyField(Task)
