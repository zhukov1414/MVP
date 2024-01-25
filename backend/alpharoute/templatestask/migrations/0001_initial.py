# Generated by Django 4.2.9 on 2024-01-25 06:03

from django.db import migrations, models
import django.db.models.deletion


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
