from django.db import models
from django.conf import settings

class Prediction(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь')
    prediction_type = models.CharField(max_length=100, verbose_name='Тип прогноза')
    current_value = models.FloatField(verbose_name='Текущее значение')
    predicted_value = models.FloatField(verbose_name='Предсказанное значение')
    prediction_date = models.DateField(verbose_name='Дата прогноза')
    target_date = models.DateField(verbose_name='Целевая дата')
    confidence = models.FloatField(verbose_name='Уверенность (%)')
    notes = models.TextField(blank=True, verbose_name='Заметки')

    class Meta:
        verbose_name = 'Прогноз'
        verbose_name_plural = 'Прогнозы'
        ordering = ['-prediction_date']

    def __str__(self):
        return f"{self.user.username} - {self.prediction_type}" 