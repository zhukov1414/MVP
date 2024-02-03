# Generated by Django 4.2.9 on 2024-02-03 05:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ipr', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL, verbose_name='Автор'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='content',
            field=models.TextField(verbose_name='Текст комментария'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='postdate',
            field=models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Дата создания'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='ipr.task', verbose_name='Задача'),
        ),
        migrations.AlterField(
            model_name='individualdevelopmentplan',
            name='deadline',
            field=models.DateField(verbose_name='Дедлайн'),
        ),
        migrations.AlterField(
            model_name='individualdevelopmentplan',
            name='description',
            field=models.TextField(verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='individualdevelopmentplan',
            name='employee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ipr_employee', to=settings.AUTH_USER_MODEL, verbose_name='Сотрудник'),
        ),
        migrations.AlterField(
            model_name='individualdevelopmentplan',
            name='goal',
            field=models.CharField(max_length=255, verbose_name='Цель'),
        ),
        migrations.AlterField(
            model_name='individualdevelopmentplan',
            name='status',
            field=models.CharField(choices=[('created', 'Создан'), ('inwork', 'В работе'), ('done', 'Выполнен'), ('checked', 'Проверен'), ('stoped', 'Приостановлен')], default='created', max_length=12, verbose_name='Статус'),
        ),
        migrations.AlterField(
            model_name='individualdevelopmentplan',
            name='title',
            field=models.CharField(max_length=255, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='task',
            name='deadline',
            field=models.DateField(blank=True, null=True, verbose_name='Дедлайн'),
        ),
        migrations.AlterField(
            model_name='task',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='task',
            name='ipr',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='task', to='ipr.individualdevelopmentplan', verbose_name='ИПР'),
        ),
        migrations.AlterField(
            model_name='task',
            name='linkURL',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Ссылка'),
        ),
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.CharField(choices=[('nocompleted', 'Не выполнено'), ('inwork', 'В работе'), ('done', 'Выполнен')], default='nocompleted', max_length=12, verbose_name='Статус'),
        ),
        migrations.AlterField(
            model_name='task',
            name='title',
            field=models.CharField(max_length=255, verbose_name='Название'),
        ),
    ]
