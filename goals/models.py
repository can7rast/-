from django.db import models
from django.conf import settings
from django.utils import timezone

class Goal(models.Model):
    """Модель для целей пользователя"""
    GOAL_TYPES = [
        ('weight', 'Вес'),
        ('workout', 'Тренировки'),
        ('nutrition', 'Питание'),
        ('sleep', 'Сон'),
        ('other', 'Другое')
    ]
    
    STATUS_CHOICES = [
        ('active', 'Активная'),
        ('completed', 'Выполнена'),
        ('failed', 'Не выполнена'),
        ('cancelled', 'Отменена')
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь')
    title = models.CharField(max_length=200, verbose_name='Название')
    description = models.TextField(blank=True, verbose_name='Описание')
    goal_type = models.CharField(max_length=20, choices=GOAL_TYPES, verbose_name='Тип цели')
    target_value = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='Целевое значение')
    current_value = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='Текущее значение')
    start_date = models.DateField(default=timezone.now, verbose_name='Дата начала')
    target_date = models.DateField(verbose_name='Целевая дата')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active', verbose_name='Статус')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Цель'
        verbose_name_plural = 'Цели'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} ({self.get_goal_type_display()})"
    
    def get_progress(self):
        """Возвращает прогресс в процентах"""
        if self.target_value and self.current_value:
            try:
                progress = (float(self.current_value) / float(self.target_value)) * 100
                return min(max(progress, 0), 100)  # Ограничиваем значение от 0 до 100
            except (ValueError, ZeroDivisionError):
                return 0
        return 0
    
    def days_remaining(self):
        """Возвращает количество оставшихся дней"""
        if self.target_date:
            today = timezone.now().date()
            remaining = (self.target_date - today).days
            return max(remaining, 0)
        return 0
    
    def is_overdue(self):
        """Проверяет, просрочена ли цель"""
        return self.target_date < timezone.now().date() and self.status == 'active' 