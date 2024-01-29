# Generated by Django 4.2.9 on 2024-01-29 19:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('postdate', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Комментарий',
                'verbose_name_plural': 'Комментарии',
                'ordering': ['-postdate'],
            },
        ),
        migrations.CreateModel(
            name='IndividualDevelopmentPlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('goal', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('deadline', models.DateField()),
                ('status', models.CharField(choices=[('created', 'Создан'), ('inwork', 'В работе'), ('done', 'Выполнен'), ('checked', 'Проверен'), ('stoped', 'Приостановлен')], default='created', max_length=12)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ipr_employee', to=settings.AUTH_USER_MODEL, verbose_name='сотрудник')),
            ],
            options={
                'verbose_name': 'Индивиуальный план развития',
                'verbose_name_plural': 'Планы развития',
            },
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('linkURL', models.CharField(blank=True, max_length=255, null=True)),
                ('deadline', models.DateField(blank=True, null=True)),
                ('status', models.CharField(choices=[('nocompleted', 'Не выполнено'), ('inwork', 'В работе'), ('done', 'Выполнен')], default='nocompleted', max_length=12)),
                ('comments', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasks_comments', to='ipr.comment')),
                ('ipr', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='task', to='ipr.individualdevelopmentplan')),
            ],
            options={
                'verbose_name': 'Задача',
                'verbose_name_plural': 'Задачи',
            },
        ),
    ]
