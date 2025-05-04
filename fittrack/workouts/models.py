from django.db import models
from django.utils.translation import gettext_lazy as _
from fittrack.users.models import User

class WorkoutType(models.Model):
    name = models.CharField(_('название'), max_length=100)
    description = models.TextField(_('описание'), blank=True)
    
    class Meta:
        verbose_name = _('тип тренировки')
        verbose_name_plural = _('типы тренировок')
    
    def __str__(self):
        return self.name

class Workout(models.Model):
    INTENSITY_CHOICES = [
        ('low', _('низкая')),
        ('medium', _('средняя')),
        ('high', _('высокая')),
    ]
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='workouts',
        verbose_name=_('пользователь')
    )
    workout_type = models.ForeignKey(
        WorkoutType,
        on_delete=models.PROTECT,
        verbose_name=_('тип тренировки')
    )
    date = models.DateTimeField(_('дата и время'))
    duration = models.DurationField(_('продолжительность'))
    intensity = models.CharField(
        _('интенсивность'),
        max_length=10,
        choices=INTENSITY_CHOICES
    )
    notes = models.TextField(_('заметки'), blank=True)
    calories_burned = models.PositiveIntegerField(
        _('сожжено калорий'),
        null=True,
        blank=True
    )
    
    class Meta:
        verbose_name = _('тренировка')
        verbose_name_plural = _('тренировки')
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.user.username} - {self.workout_type.name} ({self.date})" 