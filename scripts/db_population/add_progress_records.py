import os
import sys
import django
import random
from datetime import datetime, timedelta

# Добавляем путь к корневой директории проекта
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fittrack.settings')
django.setup()

from django.contrib.auth import get_user_model
from progress.models import Progress
from workouts.models import Workout
from django.db.models import Max

User = get_user_model()

def add_progress_data(user, start_date, end_date):
    """Добавляет данные о прогрессе с реалистичной динамикой"""
    # Начальные значения
    current_weight = 75.0  # Начальный вес
    current_chest = 98.0   # Начальные обхваты
    current_waist = 82.0
    current_hips = 98.0
    current_biceps = 34.0
    
    # Целевые значения (небольшое улучшение за период)
    target_weight = 73.0
    target_chest = 100.0
    target_waist = 80.0
    target_hips = 97.0
    target_biceps = 35.0
    
    # Количество дней между измерениями
    days_total = (end_date - start_date).days
    measurements_count = days_total // 3  # Измерения каждые 3 дня
    
    # Вычисляем изменения за одно измерение
    weight_change = (target_weight - current_weight) / measurements_count
    chest_change = (target_chest - current_chest) / measurements_count
    waist_change = (target_waist - current_waist) / measurements_count
    hips_change = (target_hips - current_hips) / measurements_count
    biceps_change = (target_biceps - current_biceps) / measurements_count
    
    current_date = start_date
    measurement_count = 0
    
    while current_date <= end_date:
        # Добавляем случайные колебания
        weight = current_weight + random.uniform(-0.3, 0.3)
        chest = current_chest + random.uniform(-0.2, 0.2)
        waist = current_waist + random.uniform(-0.2, 0.2)
        hips = current_hips + random.uniform(-0.2, 0.2)
        biceps = current_biceps + random.uniform(-0.1, 0.1)
        
        progress = Progress(
            user=user,
            date=current_date,
            weight=round(weight, 1),
            chest=round(chest, 1),
            waist=round(waist, 1),
            hips=round(hips, 1),
            biceps=round(biceps, 1),
            notes=f"Регулярное измерение {current_date.strftime('%d.%m.%Y')}"
        )
        progress.save()
        
        # Обновляем текущие значения с учетом прогресса
        current_weight += weight_change
        current_chest += chest_change
        current_waist += waist_change
        current_hips += hips_change
        current_biceps += biceps_change
        
        measurement_count += 1
        current_date += timedelta(days=3)
        
        print(f"Добавлен прогресс за {current_date}: Вес={round(weight, 1)}, Грудь={round(chest, 1)}, "
              f"Талия={round(waist, 1)}, Бедра={round(hips, 1)}, Бицепс={round(biceps, 1)}")

def calculate_personal_records(user):
    """Вычисляет и выводит личные рекорды на основе тренировок"""
    # Находим самые длительные тренировки по типам
    workout_types = ['cardio', 'strength', 'hiit', 'yoga', 'stretching']
    
    print("\nЛичные рекорды по длительности тренировок:")
    for workout_type in workout_types:
        max_duration = Workout.objects.filter(
            user=user,
            workout_type=workout_type
        ).aggregate(Max('duration'))['duration__max']
        
        if max_duration:
            workout = Workout.objects.filter(
                user=user,
                workout_type=workout_type,
                duration=max_duration
            ).first()
            
            print(f"{workout.get_workout_type_display()}: "
                  f"{max_duration} минут ({workout.date.strftime('%d.%m.%Y')})")
    
    # Находим тренировки с максимальным сжиганием калорий
    max_calories = Workout.objects.filter(user=user).aggregate(
        Max('calories_burned'))['calories_burned__max']
    if max_calories:
        workout = Workout.objects.filter(
            user=user,
            calories_burned=max_calories
        ).first()
        print(f"\nРекорд по сожженным калориям: {max_calories} ккал "
              f"({workout.get_workout_type_display()} - {workout.date.strftime('%d.%m.%Y')})")

def main():
    try:
        user = User.objects.get(username='gege')
        start_date = datetime(2025, 5, 1).date()
        end_date = datetime(2025, 6, 5).date()
        
        print("Начинаем добавление данных о прогрессе...")
        add_progress_data(user, start_date, end_date)
        
        print("\nВычисляем личные рекорды...")
        calculate_personal_records(user)
        
        print("\nВсе данные успешно добавлены!")
        
    except User.DoesNotExist:
        print("Пользователь 'gege' не найден!")
        return

if __name__ == '__main__':
    main() 