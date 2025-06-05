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

class PersonalRecord(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь')
    date = models.DateField(verbose_name='Дата')
    exercise = models.CharField(max_length=100, verbose_name='Упражнение')
    weight = models.FloatField(verbose_name='Вес (кг)')
    reps = models.IntegerField(verbose_name='Количество повторений')
    notes = models.TextField(blank=True, verbose_name='Заметки')

    class Meta:
        verbose_name = 'Личный рекорд'
        verbose_name_plural = 'Личные рекорды'
        ordering = ['-date']

    def __str__(self):
        return f"{self.user.username} - {self.exercise} ({self.date})" 