# Generated by Django 5.2.2 on 2025-06-05 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Prediction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prediction_type', models.CharField(max_length=100, verbose_name='Тип прогноза')),
                ('current_value', models.FloatField(verbose_name='Текущее значение')),
                ('predicted_value', models.FloatField(verbose_name='Предсказанное значение')),
                ('prediction_date', models.DateField(verbose_name='Дата прогноза')),
                ('target_date', models.DateField(verbose_name='Целевая дата')),
                ('confidence', models.FloatField(verbose_name='Уверенность (%)')),
                ('notes', models.TextField(blank=True, verbose_name='Заметки')),
            ],
            options={
                'verbose_name': 'Прогноз',
                'verbose_name_plural': 'Прогнозы',
                'ordering': ['-prediction_date'],
            },
        ),
    ]
