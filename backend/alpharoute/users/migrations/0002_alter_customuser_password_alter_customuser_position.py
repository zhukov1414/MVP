# Generated by Django 4.2.9 on 2024-02-03 05:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='password',
            field=models.CharField(max_length=150, verbose_name='Пароль'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='position',
            field=models.CharField(max_length=150, verbose_name='Должность'),
        ),
    ]
