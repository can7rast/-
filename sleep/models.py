from django.db import models
from django.conf import settings

class Sleep(models.Model):
    QUALITY_CHOICES = [
        ('отличный', 'Отличный'),
        ('хороший', 'Хороший'),
        ('средний', 'Средний'),
        ('плохой', 'Плохой'),
        ('очень плохой', 'Очень плохой')
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь')
    date = models.DateField(verbose_name='Дата')
    start_time = models.TimeField(verbose_name='Время отхода ко сну')
    end_time = models.TimeField(verbose_name='Время пробуждения')
    duration = models.FloatField(verbose_name='Длительность (часы)')
    quality = models.CharField(
        max_length=50,
        choices=QUALITY_CHOICES,
        verbose_name='Качество сна'
    )
    interruptions = models.IntegerField(verbose_name='Количество пробуждений', default=0)
    notes = models.TextField(blank=True, verbose_name='Заметки')

    class Meta:
        verbose_name = 'Сон'
        verbose_name_plural = 'Сон'
        ordering = ['-date']

    def __str__(self):
        return f"{self.user.username} - {self.date}" 