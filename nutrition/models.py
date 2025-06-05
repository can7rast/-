from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
import calendar

class Meal(models.Model):
    MEAL_TYPES = [
        ('breakfast', 'Завтрак'),
        ('lunch', 'Обед'),
        ('snack', 'Перекус'),
        ('dinner', 'Ужин')
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь')
    date = models.DateField(verbose_name='Дата')
    time = models.TimeField(verbose_name='Время')
    meal_type = models.CharField(
        max_length=50,
        choices=MEAL_TYPES,
        verbose_name='Тип приема пищи'
    )
    calories = models.IntegerField(verbose_name='Калории')
    protein = models.FloatField(verbose_name='Белки (г)')
    fat = models.FloatField(verbose_name='Жиры (г)')
    carbs = models.FloatField(verbose_name='Углеводы (г)')
    notes = models.TextField(blank=True, verbose_name='Заметки')

    class Meta:
        verbose_name = 'Прием пищи'
        verbose_name_plural = 'Питание'
        ordering = ['-date', '-time']

    def __str__(self):
        return f"{self.get_meal_type_display()} - {self.date}"

    @property
    def total_macros(self):
        """Возвращает общее количество макронутриентов"""
        return self.protein + self.fat + self.carbs

    @property
    def macros_percentages(self):
        """Возвращает процентное соотношение макронутриентов"""
        total = self.total_macros
        if total == 0:
            return {'protein': 0, 'fat': 0, 'carbs': 0}
        
        return {
            'protein': round((self.protein / total) * 100),
            'fat': round((self.fat / total) * 100),
            'carbs': round((self.carbs / total) * 100)
        }

class WeeklyNutritionStats(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь')
    week_start = models.DateField(verbose_name='Начало недели')
    week_end = models.DateField(verbose_name='Конец недели')
    
    # Общая статистика
    total_calories = models.IntegerField(default=0, verbose_name='Всего калорий')
    avg_daily_calories = models.FloatField(default=0, verbose_name='Среднее калорий в день')
    total_protein = models.FloatField(default=0, verbose_name='Всего белков (г)')
    total_fat = models.FloatField(default=0, verbose_name='Всего жиров (г)')
    total_carbs = models.FloatField(default=0, verbose_name='Всего углеводов (г)')
    
    # Статистика по типам приемов пищи
    breakfast_count = models.IntegerField(default=0, verbose_name='Количество завтраков')
    lunch_count = models.IntegerField(default=0, verbose_name='Количество обедов')
    snack_count = models.IntegerField(default=0, verbose_name='Количество перекусов')
    dinner_count = models.IntegerField(default=0, verbose_name='Количество ужинов')
    
    # Средние значения по приемам пищи
    avg_breakfast_calories = models.FloatField(default=0, verbose_name='Среднее калорий на завтрак')
    avg_lunch_calories = models.FloatField(default=0, verbose_name='Среднее калорий на обед')
    avg_snack_calories = models.FloatField(default=0, verbose_name='Среднее калорий на перекус')
    avg_dinner_calories = models.FloatField(default=0, verbose_name='Среднее калорий на ужин')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Недельная статистика питания'
        verbose_name_plural = 'Недельная статистика питания'
        unique_together = ['user', 'week_start']
        ordering = ['-week_start']

    def __str__(self):
        return f"Статистика {self.user.username} за неделю {self.week_start}"

    @classmethod
    def calculate_for_week(cls, user, date):
        """Рассчитывает или обновляет статистику за неделю"""
        # Находим начало и конец недели
        week_start = date - timedelta(days=date.weekday())
        week_end = week_start + timedelta(days=6)
        
        # Получаем все приемы пищи за неделю
        meals = Meal.objects.filter(
            user=user,
            date__range=[week_start, week_end]
        )
        
        # Базовая статистика
        stats = {
            'total_calories': meals.aggregate(total=models.Sum('calories'))['total'] or 0,
            'total_protein': meals.aggregate(total=models.Sum('protein'))['total'] or 0,
            'total_fat': meals.aggregate(total=models.Sum('fat'))['total'] or 0,
            'total_carbs': meals.aggregate(total=models.Sum('carbs'))['total'] or 0,
        }
        
        # Статистика по типам
        for meal_type, _ in Meal.MEAL_TYPES:
            type_meals = meals.filter(meal_type=meal_type)
            count = type_meals.count()
            avg_calories = type_meals.aggregate(avg=models.Avg('calories'))['avg'] or 0
            
            stats[f'{meal_type}_count'] = count
            stats[f'avg_{meal_type}_calories'] = round(avg_calories, 1)
        
        # Среднее количество калорий в день
        days_with_meals = meals.dates('date', 'day').count()
        stats['avg_daily_calories'] = round(stats['total_calories'] / max(days_with_meals, 1), 1)
        
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

class MonthlyNutritionStats(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь')
    year = models.IntegerField(verbose_name='Год')
    month = models.IntegerField(verbose_name='Месяц')
    
    # Общая статистика
    total_calories = models.IntegerField(default=0, verbose_name='Всего калорий')
    avg_daily_calories = models.FloatField(default=0, verbose_name='Среднее калорий в день')
    total_protein = models.FloatField(default=0, verbose_name='Всего белков (г)')
    total_fat = models.FloatField(default=0, verbose_name='Всего жиров (г)')
    total_carbs = models.FloatField(default=0, verbose_name='Всего углеводов (г)')
    
    # Статистика по типам приемов пищи
    breakfast_count = models.IntegerField(default=0, verbose_name='Количество завтраков')
    lunch_count = models.IntegerField(default=0, verbose_name='Количество обедов')
    snack_count = models.IntegerField(default=0, verbose_name='Количество перекусов')
    dinner_count = models.IntegerField(default=0, verbose_name='Количество ужинов')
    
    # Средние значения по приемам пищи
    avg_breakfast_calories = models.FloatField(default=0, verbose_name='Среднее калорий на завтрак')
    avg_lunch_calories = models.FloatField(default=0, verbose_name='Среднее калорий на обед')
    avg_snack_calories = models.FloatField(default=0, verbose_name='Среднее калорий на перекус')
    avg_dinner_calories = models.FloatField(default=0, verbose_name='Среднее калорий на ужин')

    # Дополнительная статистика
    days_tracked = models.IntegerField(default=0, verbose_name='Дней с записями')
    most_common_meal_type = models.CharField(max_length=50, blank=True, verbose_name='Самый частый прием пищи')
    highest_calorie_day = models.DateField(null=True, blank=True, verbose_name='День с максимальными калориями')
    max_daily_calories = models.IntegerField(default=0, verbose_name='Максимум калорий за день')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Месячная статистика питания'
        verbose_name_plural = 'Месячная статистика питания'
        unique_together = ['user', 'year', 'month']
        ordering = ['-year', '-month']

    def __str__(self):
        return f"Статистика {self.user.username} за {calendar.month_name[self.month]} {self.year}"

    @classmethod
    def calculate_for_month(cls, user, date):
        """Рассчитывает или обновляет статистику за месяц"""
        year = date.year
        month = date.month
        
        # Находим начало и конец месяца
        _, last_day = calendar.monthrange(year, month)
        month_start = date.replace(day=1)
        month_end = date.replace(day=last_day)
        
        # Получаем все приемы пищи за месяц
        meals = Meal.objects.filter(
            user=user,
            date__year=year,
            date__month=month
        )
        
        # Базовая статистика
        stats = {
            'total_calories': meals.aggregate(total=models.Sum('calories'))['total'] or 0,
            'total_protein': meals.aggregate(total=models.Sum('protein'))['total'] or 0,
            'total_fat': meals.aggregate(total=models.Sum('fat'))['total'] or 0,
            'total_carbs': meals.aggregate(total=models.Sum('carbs'))['total'] or 0,
        }
        
        # Статистика по типам
        meal_counts = {}
        for meal_type, _ in Meal.MEAL_TYPES:
            type_meals = meals.filter(meal_type=meal_type)
            count = type_meals.count()
            avg_calories = type_meals.aggregate(avg=models.Avg('calories'))['avg'] or 0
            
            stats[f'{meal_type}_count'] = count
            stats[f'avg_{meal_type}_calories'] = round(avg_calories, 1)
            meal_counts[meal_type] = count
        
        # Находим самый частый тип приема пищи
        if meal_counts:
            stats['most_common_meal_type'] = max(meal_counts.items(), key=lambda x: x[1])[0]
        
        # Статистика по дням
        days_with_meals = meals.dates('date', 'day')
        stats['days_tracked'] = days_with_meals.count()
        
        # Находим день с максимальными калориями
        daily_calories = {}
        for meal in meals:
            if meal.date not in daily_calories:
                daily_calories[meal.date] = 0
            daily_calories[meal.date] += meal.calories
        
        if daily_calories:
            max_day = max(daily_calories.items(), key=lambda x: x[1])
            stats['highest_calorie_day'] = max_day[0]
            stats['max_daily_calories'] = max_day[1]
        
        # Среднее количество калорий в день
        stats['avg_daily_calories'] = round(stats['total_calories'] / max(stats['days_tracked'], 1), 1)
        
        # Создаем или обновляем запись
        stats_obj, _ = cls.objects.update_or_create(
            user=user,
            year=year,
            month=month,
            defaults=stats
        )
        
        return stats_obj 