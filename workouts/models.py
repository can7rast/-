from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
import calendar


class Workout(models.Model):
    """Тренировка"""
    WORKOUT_TYPES = [
        ('cardio', 'Кардио'),
        ('strength', 'Силовая'),
        ('hiit', 'HIIT'),
        ('yoga', 'Йога'),
        ('stretching', 'Растяжка'),
        ('other', 'Другое')
    ]

    INTENSITY_LEVELS = [
        ('low', 'Низкая'),
        ('medium', 'Средняя'),
        ('high', 'Высокая')
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь')
    date = models.DateField(verbose_name='Дата')
    workout_type = models.CharField(max_length=20, choices=WORKOUT_TYPES, verbose_name='Тип тренировки')
    duration = models.IntegerField(verbose_name='Продолжительность (мин)')
    intensity = models.CharField(max_length=10, choices=INTENSITY_LEVELS, verbose_name='Интенсивность')
    calories_burned = models.IntegerField(verbose_name='Сожжено калорий')
    notes = models.TextField(blank=True, verbose_name='Заметки')

    class Meta:
        verbose_name = 'Тренировка'
        verbose_name_plural = 'Тренировки'
        ordering = ['-date']

    def __str__(self):
        return f"{self.get_workout_type_display()} - {self.date}"

    def calculate_calories(self):
        """Рассчитывает примерное количество сожженных калорий"""
        base_calories = {
            'cardio': 8,  # калорий в минуту при средней интенсивности
            'strength': 6,
            'hiit': 10,
            'yoga': 4,
            'stretching': 3,
            'other': 5
        }
        
        intensity_multiplier = {
            'low': 0.8,
            'medium': 1.0,
            'high': 1.2
        }
        
        return int(
            self.duration * 
            base_calories[self.workout_type] * 
            intensity_multiplier[self.intensity]
        )


class WeeklyWorkoutStats(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь')
    week_start = models.DateField(verbose_name='Начало недели')
    week_end = models.DateField(verbose_name='Конец недели')
    
    # Общая статистика
    total_workouts = models.IntegerField(default=0, verbose_name='Всего тренировок')
    total_duration = models.IntegerField(default=0, verbose_name='Общая продолжительность (мин)')
    total_calories = models.IntegerField(default=0, verbose_name='Всего сожжено калорий')
    avg_duration = models.FloatField(default=0, verbose_name='Средняя продолжительность (мин)')
    
    # Статистика по типам
    cardio_count = models.IntegerField(default=0, verbose_name='Кардио тренировок')
    strength_count = models.IntegerField(default=0, verbose_name='Силовых тренировок')
    hiit_count = models.IntegerField(default=0, verbose_name='HIIT тренировок')
    yoga_count = models.IntegerField(default=0, verbose_name='Йога тренировок')
    stretching_count = models.IntegerField(default=0, verbose_name='Растяжка тренировок')
    other_count = models.IntegerField(default=0, verbose_name='Других тренировок')
    
    # Средние значения по типам
    avg_cardio_duration = models.FloatField(default=0, verbose_name='Среднее время кардио (мин)')
    avg_strength_duration = models.FloatField(default=0, verbose_name='Среднее время силовых (мин)')
    avg_hiit_duration = models.FloatField(default=0, verbose_name='Среднее время HIIT (мин)')
    avg_yoga_duration = models.FloatField(default=0, verbose_name='Среднее время йоги (мин)')
    avg_stretching_duration = models.FloatField(default=0, verbose_name='Среднее время растяжки (мин)')
    avg_other_duration = models.FloatField(default=0, verbose_name='Среднее время других (мин)')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Недельная статистика тренировок'
        verbose_name_plural = 'Недельная статистика тренировок'
        unique_together = ['user', 'week_start']
        ordering = ['-week_start']

    def __str__(self):
        return f"Статистика тренировок {self.user.username} за неделю {self.week_start}"

    @classmethod
    def calculate_for_week(cls, user, date):
        """Рассчитывает или обновляет статистику за неделю"""
        # Находим начало и конец недели
        week_start = date - timedelta(days=date.weekday())
        week_end = week_start + timedelta(days=6)
        
        # Получаем все тренировки за неделю
        workouts = Workout.objects.filter(
            user=user,
            date__range=[week_start, week_end]
        )
        
        # Базовая статистика
        total_workouts = workouts.count()
        total_duration = workouts.aggregate(total=models.Sum('duration'))['total'] or 0
        total_calories = workouts.aggregate(total=models.Sum('calories_burned'))['total'] or 0
        
        stats = {
            'total_workouts': total_workouts,
            'total_duration': total_duration,
            'total_calories': total_calories,
            'avg_duration': round(total_duration / max(total_workouts, 1), 1)
        }
        
        # Статистика по типам
        for workout_type, _ in Workout.WORKOUT_TYPES:
            type_workouts = workouts.filter(workout_type=workout_type)
            count = type_workouts.count()
            avg_duration = type_workouts.aggregate(avg=models.Avg('duration'))['avg'] or 0
            
            stats[f'{workout_type}_count'] = count
            stats[f'avg_{workout_type}_duration'] = round(avg_duration, 1)
        
        # Создаем или обновляем запись
        stats_obj, _ = cls.objects.update_or_create(
            user=user,
            week_start=week_start,
            defaults={
                'week_end': week_end,
                **stats
            }
        )
        
        return stats_obj


class MonthlyWorkoutStats(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь')
    year = models.IntegerField(verbose_name='Год')
    month = models.IntegerField(verbose_name='Месяц')
    
    # Общая статистика
    total_workouts = models.IntegerField(default=0, verbose_name='Всего тренировок')
    total_duration = models.IntegerField(default=0, verbose_name='Общая продолжительность (мин)')
    total_calories = models.IntegerField(default=0, verbose_name='Всего сожжено калорий')
    avg_duration = models.FloatField(default=0, verbose_name='Средняя продолжительность (мин)')
    
    # Статистика по типам
    cardio_count = models.IntegerField(default=0, verbose_name='Кардио тренировок')
    strength_count = models.IntegerField(default=0, verbose_name='Силовых тренировок')
    hiit_count = models.IntegerField(default=0, verbose_name='HIIT тренировок')
    yoga_count = models.IntegerField(default=0, verbose_name='Йога тренировок')
    stretching_count = models.IntegerField(default=0, verbose_name='Растяжка тренировок')
    other_count = models.IntegerField(default=0, verbose_name='Других тренировок')
    
    # Средние значения
    avg_cardio_duration = models.FloatField(default=0, verbose_name='Среднее время кардио (мин)')
    avg_strength_duration = models.FloatField(default=0, verbose_name='Среднее время силовых (мин)')
    avg_hiit_duration = models.FloatField(default=0, verbose_name='Среднее время HIIT (мин)')
    avg_yoga_duration = models.FloatField(default=0, verbose_name='Среднее время йоги (мин)')
    avg_stretching_duration = models.FloatField(default=0, verbose_name='Среднее время растяжки (мин)')
    avg_other_duration = models.FloatField(default=0, verbose_name='Среднее время других (мин)')
    
    # Дополнительная статистика
    days_with_workouts = models.IntegerField(default=0, verbose_name='Дней с тренировками')
    most_common_type = models.CharField(max_length=20, blank=True, verbose_name='Самый частый тип')
    longest_workout_date = models.DateField(null=True, blank=True, verbose_name='Дата самой длинной тренировки')
    longest_workout_duration = models.IntegerField(default=0, verbose_name='Длительность самой длинной тренировки')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Месячная статистика тренировок'
        verbose_name_plural = 'Месячная статистика тренировок'
        unique_together = ['user', 'year', 'month']
        ordering = ['-year', '-month']

    def __str__(self):
        return f"Статистика тренировок {self.user.username} за {calendar.month_name[self.month]} {self.year}"

    @classmethod
    def calculate_for_month(cls, user, date):
        """Рассчитывает или обновляет статистику за месяц"""
        year = date.year
        month = date.month
        
        # Получаем все тренировки за месяц
        workouts = Workout.objects.filter(
            user=user,
            date__year=year,
            date__month=month
        )
        
        # Базовая статистика
        total_workouts = workouts.count()
        total_duration = workouts.aggregate(total=models.Sum('duration'))['total'] or 0
        total_calories = workouts.aggregate(total=models.Sum('calories_burned'))['total'] or 0
        
        stats = {
            'total_workouts': total_workouts,
            'total_duration': total_duration,
            'total_calories': total_calories,
            'avg_duration': round(total_duration / max(total_workouts, 1), 1)
        }
        
        # Статистика по типам
        workout_counts = {}
        for workout_type, _ in Workout.WORKOUT_TYPES:
            type_workouts = workouts.filter(workout_type=workout_type)
            count = type_workouts.count()
            avg_duration = type_workouts.aggregate(avg=models.Avg('duration'))['avg'] or 0
            
            stats[f'{workout_type}_count'] = count
            stats[f'avg_{workout_type}_duration'] = round(avg_duration, 1)
            workout_counts[workout_type] = count
        
        # Находим самый частый тип тренировок
        if workout_counts:
            stats['most_common_type'] = max(workout_counts.items(), key=lambda x: x[1])[0]
        
        # Статистика по дням
        stats['days_with_workouts'] = workouts.dates('date', 'day').count()
        
        # Находим самую длинную тренировку
        if workouts.exists():
            longest_workout = workouts.order_by('-duration').first()
            stats['longest_workout_date'] = longest_workout.date
            stats['longest_workout_duration'] = longest_workout.duration
        
        # Создаем или обновляем запись
        stats_obj, _ = cls.objects.update_or_create(
            user=user,
            year=year,
            month=month,
            defaults=stats
        )
        
        return stats_obj 