from django.db import models
from django.utils.translation import gettext_lazy as _
from fittrack.users.models import User

class Meal(models.Model):
    MEAL_TYPE_CHOICES = [
        ('breakfast', _('завтрак')),
        ('lunch', _('обед')),
        ('dinner', _('ужин')),
        ('snack', _('перекус')),
    ]
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='meals',
        verbose_name=_('пользователь')
    )
    date = models.DateField(_('дата'))
    meal_type = models.CharField(
        _('тип приема пищи'),
        max_length=20,
        choices=MEAL_TYPE_CHOICES
    )
    time = models.TimeField(_('время'))
    calories = models.PositiveIntegerField(_('калории'))
    protein = models.DecimalField(
        _('белки'),
        max_digits=5,
        decimal_places=1,
        help_text=_('граммы')
    )
    fat = models.DecimalField(
        _('жиры'),
        max_digits=5,
        decimal_places=1,
        help_text=_('граммы')
    )
    carbs = models.DecimalField(
        _('углеводы'),
        max_digits=5,
        decimal_places=1,
        help_text=_('граммы')
    )
    notes = models.TextField(_('заметки'), blank=True)
    
    class Meta:
        verbose_name = _('прием пищи')
        verbose_name_plural = _('приемы пищи')
        ordering = ['-date', '-time']
    
    def __str__(self):
        return f"{self.user.username} - {self.get_meal_type_display()} ({self.date})" 