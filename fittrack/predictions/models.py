from django.db import models
from django.utils.translation import gettext_lazy as _
from fittrack.users.models import User

class Prediction(models.Model):
    PREDICTION_TYPE_CHOICES = [
        ('weight', _('вес')),
        ('strength', _('сила')),
        ('endurance', _('выносливость')),
        ('body_fat', _('процент жира')),
    ]
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='predictions',
        verbose_name=_('пользователь')
    )
    prediction_type = models.CharField(
        _('тип прогноза'),
        max_length=20,
        choices=PREDICTION_TYPE_CHOICES
    )
    current_value = models.DecimalField(
        _('текущее значение'),
        max_digits=10,
        decimal_places=2
    )
    predicted_value = models.DecimalField(
        _('прогнозируемое значение'),
        max_digits=10,
        decimal_places=2
    )
    prediction_date = models.DateField(_('дата прогноза'))
    target_date = models.DateField(_('целевая дата'))
    confidence = models.DecimalField(
        _('уверенность прогноза'),
        max_digits=5,
        decimal_places=2,
        help_text=_('процент')
    )
    notes = models.TextField(_('заметки'), blank=True)
    
    class Meta:
        verbose_name = _('прогноз')
        verbose_name_plural = _('прогнозы')
        ordering = ['-prediction_date']
    
    def __str__(self):
        return f"{self.user.username} - {self.get_prediction_type_display()} ({self.prediction_date})" 