from django.db import models
from django.conf import settings


class WorkoutType(models.Model):
    """Тип тренировки"""
    name = models.CharField(max_length=100, verbose_name='Название')
    description = models.TextField(blank=True, verbose_name='Описание')
    calories_per_hour = models.IntegerField(verbose_name='Калории в час')

    class Meta:
        verbose_name = 'Тип тренировки'
        verbose_name_plural = 'Типы тренировок'

    def __str__(self):
        return self.name


class Workout(models.Model):
    """Тренировка"""
    INTENSITY_CHOICES = [
        ('low', 'Низкая'),
        ('medium', 'Средняя'),
        ('high', 'Высокая'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь')
    workout_type = models.ForeignKey(WorkoutType, on_delete=models.CASCADE, verbose_name='Тип тренировки')
    date = models.DateField(verbose_name='Дата')
    duration = models.DurationField(verbose_name='Продолжительность')
    intensity = models.CharField(
        max_length=10,
        choices=INTENSITY_CHOICES,
        default='medium',
        verbose_name='Интенсивность'
    )
    calories_burned = models.IntegerField(verbose_name='Сожжено калорий')
    notes = models.TextField(blank=True, verbose_name='Заметки')

    class Meta:
        verbose_name = 'Тренировка'
        verbose_name_plural = 'Тренировки'
        ordering = ['-date']

    def __str__(self):
        return f"{self.workout_type.name} - {self.date}"

    def save(self, *args, **kwargs):
        # Автоматический расчет калорий
        hours = self.duration.total_seconds() / 3600
        self.calories_burned = int(hours * self.workout_type.calories_per_hour)
        super().save(*args, **kwargs) 