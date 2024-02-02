# Generated by Django 4.2.9 on 2024-02-01 23:09

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ipr', '0002_alter_task_comments'),
    ]

    operations = [
        migrations.AddField(
            model_name='individualdevelopmentplan',
            name='progress',
            field=models.PositiveIntegerField(default=0, validators=[django.core.validators.MaxValueValidator(100)]),
        ),
    ]
