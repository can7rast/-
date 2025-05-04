from django.db import models
from django.conf import settings

class Progress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь')
    date = models.DateField(verbose_name='Дата')
    weight = models.FloatField(verbose_name='Вес (кг)')
    chest = models.FloatField(verbose_name='Грудь (см)', null=True, blank=True)
    waist = models.FloatField(verbose_name='Талия (см)', null=True, blank=True)
    hips = models.FloatField(verbose_name='Бедра (см)', null=True, blank=True)
    biceps = models.FloatField(verbose_name='Бицепс (см)', null=True, blank=True)
    notes = models.TextField(blank=True, verbose_name='Заметки')

    class Meta:
        verbose_name = 'Прогресс'
        verbose_name_plural = 'Прогресс'
        ordering = ['-date']

    def __str__(self):
        return f"{self.user.username} - {self.date}" 