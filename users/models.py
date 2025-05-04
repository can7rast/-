from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class User(AbstractUser):
    is_coach = models.BooleanField(
        _('тренер'),
        default=False,
        help_text=_('Определяет, является ли пользователь тренером')
    )
    
    class Meta:
        verbose_name = _('пользователь')
        verbose_name_plural = _('пользователи')
        ordering = ['-date_joined']

class Profile(models.Model):
    ROLE_CHOICES = (
        ('athlete', 'Спортсмен'),
        ('coach', 'Тренер'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    bio = models.TextField(max_length=500, blank=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='athlete')

    def __str__(self):
        return f'{self.user.username} Profile'

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()

class CoachAthlete(models.Model):
    coach = models.ForeignKey(User, on_delete=models.CASCADE, related_name='coach_athletes')
    athlete = models.ForeignKey(User, on_delete=models.CASCADE, related_name='athlete_coaches')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('coach', 'athlete')

    def __str__(self):
        return f'{self.coach.username} - {self.athlete.username}' 