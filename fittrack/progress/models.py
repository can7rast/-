from django.db import models
from django.utils.translation import gettext_lazy as _
from fittrack.users.models import User

class Progress(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='progress_records',
        verbose_name=_('пользователь')
    )
    date = models.DateField(_('дата'))
    weight = models.DecimalField(
        _('вес'),
        max_digits=5,
        decimal_places=1,
        help_text=_('килограммы')
    )
    chest = models.DecimalField(
        _('грудь'),
        max_digits=5,
        decimal_places=1,
        help_text=_('сантиметры'),
        null=True,
        blank=True
    )
    waist = models.DecimalField(
        _('талия'),
        max_digits=5,
        decimal_places=1,
        help_text=_('сантиметры'),
        null=True,
        blank=True
    )
    hips = models.DecimalField(
        _('бедра'),
        max_digits=5,
        decimal_places=1,
        help_text=_('сантиметры'),
        null=True,
        blank=True
    )
    biceps = models.DecimalField(
        _('бицепс'),
        max_digits=5,
        decimal_places=1,
        help_text=_('сантиметры'),
        null=True,
        blank=True
    )
    notes = models.TextField(_('заметки'), blank=True)
    
    class Meta:
        verbose_name = _('запись прогресса')
        verbose_name_plural = _('записи прогресса')
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.user.username} - {self.date}"

class PersonalRecord(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='personal_records',
        verbose_name=_('пользователь')
    )
    exercise = models.CharField(_('упражнение'), max_length=100)
    weight = models.DecimalField(
        _('вес'),
        max_digits=5,
        decimal_places=1,
        help_text=_('килограммы')
    )
    reps = models.PositiveIntegerField(_('повторения'))
    date = models.DateField(_('дата'))
    notes = models.TextField(_('заметки'), blank=True)
    
    class Meta:
        verbose_name = _('личный рекорд')
        verbose_name_plural = _('личные рекорды')
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.user.username} - {self.exercise} ({self.date})" 