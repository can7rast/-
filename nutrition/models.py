from django.db import models
from django.conf import settings

class Meal(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь')
    date = models.DateField(verbose_name='Дата')
    time = models.TimeField(verbose_name='Время')
    meal_type = models.CharField(max_length=50, verbose_name='Тип приема пищи')
    calories = models.IntegerField(verbose_name='Калории')
    protein = models.FloatField(verbose_name='Белки (г)')
    fat = models.FloatField(verbose_name='Жиры (г)')
    carbs = models.FloatField(verbose_name='Углеводы (г)')
    notes = models.TextField(blank=True, verbose_name='Заметки')

    class Meta:
        verbose_name = 'Прием пищи'
        verbose_name_plural = 'Питание'
        ordering = ['-date', '-time']

    def __str__(self):
        return f"{self.user.username} - {self.date} {self.time}" 