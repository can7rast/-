from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

class User(AbstractUser):
    is_coach = models.BooleanField(
        _('тренер'),
        default=False,
        help_text=_('Определяет, является ли пользователь тренером')
    )
    
    def __str__(self):
        return self.username

    class Meta:
        verbose_name = _('пользователь')
        verbose_name_plural = _('пользователи')
        ordering = ['-date_joined']

class Profile(models.Model):
    GENDER_CHOICES = [
        ('M', 'Мужской'),
        ('F', 'Женский'),
        ('O', 'Другой')
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='profile_pics', default='default.jpg', verbose_name='Аватар')
    birth_date = models.DateField(null=True, blank=True, verbose_name='Дата рождения')
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True, verbose_name='Пол')
    height = models.PositiveIntegerField(null=True, blank=True, verbose_name='Рост (см)')
    weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name='Вес (кг)')
    bio = models.TextField(max_length=500, blank=True, verbose_name='О себе')
    
    def __str__(self):
        return f'Профиль пользователя {self.user.username}'
    
    def get_bmi(self):
        """Вычисляет индекс массы тела"""
        if self.height and self.weight:
            height_m = self.height / 100
            bmi = float(self.weight) / (height_m * height_m)
            return round(bmi, 1)
        return None
    
    def get_bmi_status(self):
        """Возвращает статус ИМТ"""
        bmi = self.get_bmi()
        if bmi is None:
            return 'Нет данных'
        elif bmi < 18.5:
            return 'Недостаточный вес'
        elif bmi < 25:
            return 'Нормальный вес'
        elif bmi < 30:
            return 'Избыточный вес'
        else:
            return 'Ожирение'

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class CoachAthlete(models.Model):
    coach = models.ForeignKey(User, on_delete=models.CASCADE, related_name='coached_athletes')
    athlete = models.ForeignKey(User, on_delete=models.CASCADE, related_name='coaches')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('coach', 'athlete')
        verbose_name = 'Связь тренер-спортсмен'
        verbose_name_plural = 'Связи тренер-спортсмен'
    
    def __str__(self):
        return f'{self.coach.username} тренирует {self.athlete.username}' 