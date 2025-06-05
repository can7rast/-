import os
import django
import random
from datetime import datetime, timedelta, time
from django.utils import timezone

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fittrack.settings')
django.setup()

from django.contrib.auth import get_user_model
from workouts.models import Workout
from nutrition.models import Meal
from progress.models import Progress
from sleep.models import Sleep

User = get_user_model()

def create_workouts(user, start_date, end_date):
    workout_types = ['cardio', 'strength', 'hiit', 'yoga', 'stretching', 'other']
    current_date = start_date
    
    while current_date <= end_date:
        # Пропускаем некоторые дни для реалистичности
        if random.random() > 0.8:
            current_date += timedelta(days=1)
            continue
            
        workout = Workout(
            user=user,
            date=current_date,
            workout_type=random.choice(workout_types),
            duration=random.randint(30, 120),
            calories_burned=random.randint(200, 800),
            notes=f"Тренировка {current_date.strftime('%d.%m.%Y')}",
            intensity=random.choice(['low', 'medium', 'high'])
        )
        workout.save()
        current_date += timedelta(days=1)

def create_meals(user, start_date, end_date):
    meal_types = ['breakfast', 'lunch', 'dinner', 'snack']
    meals_data = [
        # (тип, калории, белки, жиры, углеводы, заметки)
        ('breakfast', 350, 20, 12, 45, 'Овсянка с фруктами'),
        ('lunch', 450, 35, 15, 55, 'Греческий салат с курицей'),
        ('dinner', 550, 40, 20, 50, 'Рыба с овощами'),
        ('snack', 200, 15, 8, 25, 'Протеиновый коктейль'),
    ]
    
    current_date = start_date
    while current_date <= end_date:
        # Создаем 3-4 приема пищи в день
        daily_meals = random.sample(meals_data, random.randint(3, 4))
        meal_times = sorted([random.randint(8, 21) for _ in range(len(daily_meals))])
        
        for i, meal_time in enumerate(meal_times):
            meal_data = daily_meals[i]
            meal = Meal(
                user=user,
                date=current_date,
                time=time(hour=meal_time),
                meal_type=meal_data[0],
                calories=meal_data[1],
                protein=meal_data[2],
                fat=meal_data[3],
                carbs=meal_data[4],
                notes=meal_data[5]
            )
            meal.save()
        
        current_date += timedelta(days=1)

def create_progress(user, start_date, end_date):
    current_date = start_date
    weight = random.uniform(70.0, 75.0)  # Начальный вес
    chest = random.uniform(95.0, 100.0)  # Начальные значения для обхватов
    waist = random.uniform(75.0, 80.0)
    hips = random.uniform(95.0, 100.0)
    biceps = random.uniform(32.0, 35.0)
    
    while current_date <= end_date:
        # Записываем прогресс каждые 3-4 дня
        if random.random() > 0.7:
            # Небольшие изменения в измерениях
            weight += random.uniform(-0.2, 0.2)
            chest += random.uniform(-0.3, 0.3)
            waist += random.uniform(-0.3, 0.3)
            hips += random.uniform(-0.3, 0.3)
            biceps += random.uniform(-0.1, 0.1)
            
            progress = Progress(
                user=user,
                date=current_date,
                weight=round(weight, 1),
                chest=round(chest, 1),
                waist=round(waist, 1),
                hips=round(hips, 1),
                biceps=round(biceps, 1),
                notes=f"Измерения за {current_date.strftime('%d.%m.%Y')}"
            )
            progress.save()
        
        current_date += timedelta(days=1)

def create_sleep_data(user, start_date, end_date):
    current_date = start_date
    
    while current_date <= end_date:
        # Генерируем случайное время отхода ко сну (между 21:00 и 00:00)
        start_hour = random.randint(21, 23)
        start_minute = random.randint(0, 59)
        start_time = time(hour=start_hour, minute=start_minute)
        
        # Генерируем случайное время пробуждения (между 6:00 и 9:00)
        end_hour = random.randint(6, 8)
        end_minute = random.randint(0, 59)
        end_time = time(hour=end_hour, minute=end_minute)
        
        # Рассчитываем длительность сна
        sleep_duration = (end_hour + 24 if start_hour > end_hour else end_hour) - start_hour + \
                        (end_minute - start_minute) / 60.0
        
        sleep = Sleep(
            user=user,
            date=current_date,
            start_time=start_time,
            end_time=end_time,
            duration=round(sleep_duration, 1),
            quality=random.choice(['отличный', 'хороший', 'средний', 'плохой', 'очень плохой']),
            interruptions=random.randint(0, 3),
            notes=f"Сон за {current_date.strftime('%d.%m.%Y')}"
        )
        sleep.save()
        
        current_date += timedelta(days=1)

def main():
    try:
        user = User.objects.get(username='gege')
        start_date = datetime(2025, 5, 1).date()
        end_date = datetime(2025, 6, 5).date()
        
        print("Начинаем заполнение базы данных...")
        
        print("Создаем записи о тренировках...")
        create_workouts(user, start_date, end_date)
        
        print("Создаем записи о питании...")
        create_meals(user, start_date, end_date)
        
        print("Создаем записи о прогрессе...")
        create_progress(user, start_date, end_date)
        
        print("Создаем записи о сне...")
        create_sleep_data(user, start_date, end_date)
        
        print("База данных успешно заполнена!")
        
    except User.DoesNotExist:
        print("Пользователь 'gege' не найден!")
        return

if __name__ == '__main__':
    main() 