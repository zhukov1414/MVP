# Generated by Django 4.2.9 on 2024-02-05 01:27

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
            name='IndividualDevelopmentPlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Название')),
                ('goal', models.CharField(max_length=255, verbose_name='Цель')),
                ('description', models.TextField(verbose_name='Описание')),
                ('deadline', models.DateField(verbose_name='Дедлайн')),
                ('status', models.CharField(choices=[('created', 'Создан'), ('inwork', 'В работе'), ('done', 'Выполнен'), ('checked', 'Проверен'), ('stoped', 'Приостановлен')], default='created', max_length=12, verbose_name='Статус')),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ipr_employee', to=settings.AUTH_USER_MODEL, verbose_name='Сотрудник')),
            ],
            options={
                'verbose_name': 'Индивиуальный план развития',
                'verbose_name_plural': 'Планы развития',
            },
        ),
        migrations.CreateModel(
            name='Template',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Название')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание')),
                ('linkURL', models.CharField(blank=True, max_length=255, null=True, verbose_name='Ссылка')),
                ('department', models.CharField(choices=[('art', 'Дизайн'), ('QA', 'QA'), ('BA', 'BA'), ('SA', 'SA')], max_length=12, verbose_name='Департамент')),
            ],
            options={
                'verbose_name': 'Шаблон',
                'verbose_name_plural': 'Шаблоны',
                'ordering': ['department'],
            },
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Название')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание')),
                ('linkURL', models.CharField(blank=True, max_length=255, null=True, verbose_name='Ссылка')),
                ('deadline', models.DateField(blank=True, null=True, verbose_name='Дедлайн')),
                ('status', models.CharField(choices=[('nocompleted', 'Не выполнено'), ('inwork', 'В работе'), ('done', 'Выполнен')], default='nocompleted', max_length=12, verbose_name='Статус')),
                ('ipr', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='task', to='ipr.individualdevelopmentplan', verbose_name='ИПР')),
            ],
            options={
                'verbose_name': 'Задача',
                'verbose_name_plural': 'Задачи',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(verbose_name='Текст комментария')),
                ('postdate', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Дата создания')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='ipr.task', verbose_name='Задача')),
            ],
            options={
                'verbose_name': 'Комментарий',
                'verbose_name_plural': 'Комментарии',
                'ordering': ['-postdate'],
            },
        ),
    ]
