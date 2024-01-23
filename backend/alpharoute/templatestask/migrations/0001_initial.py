# Generated by Django 5.0.1 on 2024-01-22 20:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.PositiveSmallIntegerField(choices=[(0, 'Дизайн'), (1, 'QA'), (2, 'BA'), (3, 'SA')], verbose_name='title')),
            ],
            options={
                'verbose_name': 'направление',
                'verbose_name_plural': 'направления',
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='Template',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('linkURL', models.CharField(blank=True, max_length=255, null=True)),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='templatestask.department')),
            ],
            options={
                'verbose_name': 'Шаблон',
                'verbose_name_plural': 'Шаблоны',
                'ordering': ['department'],
            },
        ),
    ]
