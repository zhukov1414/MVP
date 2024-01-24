# Generated by Django 5.0.1 on 2024-01-23 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ipr', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='individualdevelopmentplan',
            name='status',
            field=models.PositiveSmallIntegerField(choices=[(0, 'не выполнен'), (1, 'в работе'), (2, 'выполнен'), (3, 'проверен'), (4, 'отменен')], verbose_name='status'),
        ),
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.PositiveSmallIntegerField(choices=[(0, 'не выполнен'), (1, 'в работе'), (2, 'выполнен'), (3, 'проверен'), (4, 'отменен')], verbose_name='status'),
        ),
    ]
