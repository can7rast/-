# Generated by Django 5.2.2 on 2025-06-05 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Progress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='Дата')),
                ('weight', models.FloatField(verbose_name='Вес (кг)')),
                ('chest', models.FloatField(blank=True, null=True, verbose_name='Грудь (см)')),
                ('waist', models.FloatField(blank=True, null=True, verbose_name='Талия (см)')),
                ('hips', models.FloatField(blank=True, null=True, verbose_name='Бедра (см)')),
                ('biceps', models.FloatField(blank=True, null=True, verbose_name='Бицепс (см)')),
                ('notes', models.TextField(blank=True, verbose_name='Заметки')),
            ],
            options={
                'verbose_name': 'Прогресс',
                'verbose_name_plural': 'Прогресс',
                'ordering': ['-date'],
            },
        ),
    ]
