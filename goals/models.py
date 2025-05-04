from django.db import models
from django.conf import settings

class Goal(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь')
    goal_type = models.CharField(max_length=100, verbose_name='Тип цели')
    current_value = models.FloatField(verbose_name='Текущее значение')
    target_value = models.FloatField(verbose_name='Целевое значение')
    start_date = models.DateField(verbose_name='Дата начала')
    end_date = models.DateField(verbose_name='Дата окончания')
    status = models.CharField(max_length=20, choices=[('active', 'Активна'), ('completed', 'Выполнена'), ('failed', 'Не выполнена')], default='active', verbose_name='Статус')
    description = models.TextField(blank=True, verbose_name='Описание')
    notes = models.TextField(blank=True, verbose_name='Заметки')

    class Meta:
        verbose_name = 'Цель'
        verbose_name_plural = 'Цели'
        ordering = ['-start_date']

    def __str__(self):
        return f"{self.user.username} - {self.goal_type}" 