from django.db import models
from django.utils.translation import gettext_lazy as _
from fittrack.users.models import User

class Sleep(models.Model):
    QUALITY_CHOICES = [
        ('poor', _('плохое')),
        ('fair', _('удовлетворительное')),
        ('good', _('хорошее')),
        ('excellent', _('отличное')),
    ]
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sleep_records',
        verbose_name=_('пользователь')
    )
    date = models.DateField(_('дата'))
    start_time = models.TimeField(_('время отхода ко сну'))
    end_time = models.TimeField(_('время пробуждения'))
    duration = models.DurationField(_('продолжительность сна'))
    quality = models.CharField(
        _('качество сна'),
        max_length=20,
        choices=QUALITY_CHOICES
    )
    interruptions = models.PositiveIntegerField(
        _('количество пробуждений'),
        default=0
    )
    notes = models.TextField(_('заметки'), blank=True)
    
    class Meta:
        verbose_name = _('запись сна')
        verbose_name_plural = _('записи сна')
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.user.username} - {self.date}" 