from django.db import models
from django.utils.translation import gettext_lazy as _
from fittrack.users.models import User

class Goal(models.Model):
    GOAL_TYPE_CHOICES = [
        ('weight', _('вес')),
        ('strength', _('сила')),
        ('endurance', _('выносливость')),
        ('body_fat', _('процент жира')),
        ('measurements', _('обхваты')),
    ]
    
    STATUS_CHOICES = [
        ('active', _('активная')),
        ('completed', _('выполнена')),
        ('failed', _('не выполнена')),
    ]
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='goals',
        verbose_name=_('пользователь')
    )
    goal_type = models.CharField(
        _('тип цели'),
        max_length=20,
        choices=GOAL_TYPE_CHOICES
    )
    target_value = models.DecimalField(
        _('целевое значение'),
        max_digits=10,
        decimal_places=2
    )
    current_value = models.DecimalField(
        _('текущее значение'),
        max_digits=10,
        decimal_places=2
    )
    start_date = models.DateField(_('дата начала'))
    end_date = models.DateField(_('дата окончания'))
    status = models.CharField(
        _('статус'),
        max_length=20,
        choices=STATUS_CHOICES,
        default='active'
    )
    description = models.TextField(_('описание'))
    notes = models.TextField(_('заметки'), blank=True)
    
    class Meta:
        verbose_name = _('цель')
        verbose_name_plural = _('цели')
        ordering = ['-start_date']
    
    def __str__(self):
        return f"{self.user.username} - {self.get_goal_type_display()} ({self.start_date} - {self.end_date})" 