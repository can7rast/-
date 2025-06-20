# Generated by Django 5.2 on 2025-06-05 18:50

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workouts', '0004_merge_20250605_2141'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='workout',
            name='calories_burned',
            field=models.IntegerField(verbose_name='Сожжено калорий'),
        ),
        migrations.AlterField(
            model_name='workout',
            name='duration',
            field=models.IntegerField(verbose_name='Продолжительность (мин)'),
        ),
        migrations.AlterField(
            model_name='workout',
            name='intensity',
            field=models.CharField(choices=[('low', 'Низкая'), ('medium', 'Средняя'), ('high', 'Высокая')], max_length=10, verbose_name='Интенсивность'),
        ),
        migrations.CreateModel(
            name='MonthlyWorkoutStats',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.IntegerField(verbose_name='Год')),
                ('month', models.IntegerField(verbose_name='Месяц')),
                ('total_workouts', models.IntegerField(default=0, verbose_name='Всего тренировок')),
                ('total_duration', models.IntegerField(default=0, verbose_name='Общая продолжительность (мин)')),
                ('total_calories', models.IntegerField(default=0, verbose_name='Всего сожжено калорий')),
                ('avg_duration', models.FloatField(default=0, verbose_name='Средняя продолжительность (мин)')),
                ('cardio_count', models.IntegerField(default=0, verbose_name='Кардио тренировок')),
                ('strength_count', models.IntegerField(default=0, verbose_name='Силовых тренировок')),
                ('hiit_count', models.IntegerField(default=0, verbose_name='HIIT тренировок')),
                ('yoga_count', models.IntegerField(default=0, verbose_name='Йога тренировок')),
                ('stretching_count', models.IntegerField(default=0, verbose_name='Растяжка тренировок')),
                ('other_count', models.IntegerField(default=0, verbose_name='Других тренировок')),
                ('avg_cardio_duration', models.FloatField(default=0, verbose_name='Среднее время кардио (мин)')),
                ('avg_strength_duration', models.FloatField(default=0, verbose_name='Среднее время силовых (мин)')),
                ('avg_hiit_duration', models.FloatField(default=0, verbose_name='Среднее время HIIT (мин)')),
                ('avg_yoga_duration', models.FloatField(default=0, verbose_name='Среднее время йоги (мин)')),
                ('avg_stretching_duration', models.FloatField(default=0, verbose_name='Среднее время растяжки (мин)')),
                ('avg_other_duration', models.FloatField(default=0, verbose_name='Среднее время других (мин)')),
                ('days_with_workouts', models.IntegerField(default=0, verbose_name='Дней с тренировками')),
                ('most_common_type', models.CharField(blank=True, max_length=20, verbose_name='Самый частый тип')),
                ('longest_workout_date', models.DateField(blank=True, null=True, verbose_name='Дата самой длинной тренировки')),
                ('longest_workout_duration', models.IntegerField(default=0, verbose_name='Длительность самой длинной тренировки')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Месячная статистика тренировок',
                'verbose_name_plural': 'Месячная статистика тренировок',
                'ordering': ['-year', '-month'],
                'unique_together': {('user', 'year', 'month')},
            },
        ),
        migrations.CreateModel(
            name='WeeklyWorkoutStats',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('week_start', models.DateField(verbose_name='Начало недели')),
                ('week_end', models.DateField(verbose_name='Конец недели')),
                ('total_workouts', models.IntegerField(default=0, verbose_name='Всего тренировок')),
                ('total_duration', models.IntegerField(default=0, verbose_name='Общая продолжительность (мин)')),
                ('total_calories', models.IntegerField(default=0, verbose_name='Всего сожжено калорий')),
                ('avg_duration', models.FloatField(default=0, verbose_name='Средняя продолжительность (мин)')),
                ('cardio_count', models.IntegerField(default=0, verbose_name='Кардио тренировок')),
                ('strength_count', models.IntegerField(default=0, verbose_name='Силовых тренировок')),
                ('hiit_count', models.IntegerField(default=0, verbose_name='HIIT тренировок')),
                ('yoga_count', models.IntegerField(default=0, verbose_name='Йога тренировок')),
                ('stretching_count', models.IntegerField(default=0, verbose_name='Растяжка тренировок')),
                ('other_count', models.IntegerField(default=0, verbose_name='Других тренировок')),
                ('avg_cardio_duration', models.FloatField(default=0, verbose_name='Среднее время кардио (мин)')),
                ('avg_strength_duration', models.FloatField(default=0, verbose_name='Среднее время силовых (мин)')),
                ('avg_hiit_duration', models.FloatField(default=0, verbose_name='Среднее время HIIT (мин)')),
                ('avg_yoga_duration', models.FloatField(default=0, verbose_name='Среднее время йоги (мин)')),
                ('avg_stretching_duration', models.FloatField(default=0, verbose_name='Среднее время растяжки (мин)')),
                ('avg_other_duration', models.FloatField(default=0, verbose_name='Среднее время других (мин)')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Недельная статистика тренировок',
                'verbose_name_plural': 'Недельная статистика тренировок',
                'ordering': ['-week_start'],
                'unique_together': {('user', 'week_start')},
            },
        ),
    ]
