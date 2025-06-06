import os
import sys
import django
import random
from datetime import datetime, timedelta
import math

# Добавляем путь к корневой директории проекта
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fittrack.settings')
django.setup()

from django.contrib.auth import get_user_model
from workouts.models import Workout
from nutrition.models import Meal
from progress.models import Progress
from goals.models import Goal
from django.db import connection

User = get_user_model()

def reset_database():
    """Полностью очищает все данные из базы данных"""
    # Удаляем данные пользователя, что автоматически удалит связанные записи
    User.objects.filter(username='gege').delete()
    print("База данных очищена")

def create_test_data():
    # Создаем пользователя
    user = User.objects.create_user(
        username='gege',
        email='gege@example.com',
        password='gege123'
    )
    print("Создан новый пользователь 'gege'")

    # Устанавливаем даты
    start_date = datetime(2025, 5, 1).date()
    end_date = datetime(2025, 6, 5).date()
    current_date = start_date
    
    # Начальный вес и цель
    initial_weight = 75.0
    target_weight = 85.0
    current_weight = initial_weight

    # Создаем цель по набору массы
    Goal.objects.create(
        user=user,
        title='Набор мышечной массы',
        description='Набор массы с 75 до 85 кг через интенсивные тренировки и правильное питание',
        goal_type='weight',
        target_value=target_weight,
        current_value=initial_weight,
        start_date=start_date,
        target_date=end_date,
        status='active'
    )

    total_days = (end_date - start_date).days
    current_day = 0

    while current_date <= end_date:
        # Прогресс веса (каждый понедельник + дополнительные дни)
        if current_date.weekday() == 0 or random.random() < 0.3:
            # Линейный прогресс с небольшими колебаниями
            base_progress = initial_weight + ((target_weight - initial_weight) * (current_day / total_days))
            daily_variation = random.uniform(-0.3, 0.5)  # Больше шанс положительного отклонения
            current_weight = base_progress + daily_variation

            # Увеличение мышечной массы отражается в измерениях
            progress_factor = 1 + (current_day / total_days) * 0.12  # Максимальный прирост 12%
            
            Progress.objects.create(
                user=user,
                date=current_date,
                weight=round(current_weight, 1),
                chest=round(95 * progress_factor + random.uniform(-0.3, 0.7), 1),  # Больший прирост в груди
                waist=round(82 * (1 + (current_day / total_days) * 0.05) + random.uniform(-0.2, 0.4), 1),  # Меньший прирост талии
                hips=round(98 * progress_factor + random.uniform(-0.3, 0.5), 1),
                biceps=round(32 * (1 + (current_day / total_days) * 0.15) + random.uniform(-0.2, 0.4), 1)  # Заметный прирост бицепса
            )

        # Тренировки (5-6 раз в неделю)
        if current_date.weekday() != 6 or random.random() < 0.7:  # Тренировки даже в воскресенье с вероятностью 70%
            # Определяем тип тренировки на основе дня недели
            if current_date.weekday() in [1, 4]:  # Вторник и пятница - силовые на верх тела
                workout_type = 'strength'
                focus = 'верх тела'
                duration = random.randint(70, 85)
            elif current_date.weekday() in [2, 5]:  # Среда и суббота - силовые на низ тела
                workout_type = 'strength'
                focus = 'низ тела'
                duration = random.randint(65, 80)
            elif current_date.weekday() == 3:  # Четверг - HIIT
                workout_type = 'hiit'
                focus = 'общая'
                duration = random.randint(35, 45)
            else:  # Другие дни - кардио или йога
                workout_type = random.choice(['cardio', 'yoga'])
                focus = 'восстановление'
                duration = random.randint(40, 50)

            # Интенсивность увеличивается со временем
            base_intensity = 0.6 + (current_day / total_days) * 0.3
            intensity = 'high' if random.random() < base_intensity else 'medium'

            # Расчет сожженных калорий
            base_calories = {
                'strength': 8.5,  # Увеличенные калории для силовых
                'hiit': 12,
                'cardio': 10,
                'yoga': 5
            }
            intensity_multiplier = {'medium': 1.0, 'high': 1.4}
            calories_burned = int(duration * base_calories[workout_type] * intensity_multiplier[intensity])

            Workout.objects.create(
                user=user,
                date=current_date,
                workout_type=workout_type,
                duration=duration,
                intensity=intensity,
                calories_burned=calories_burned,
                notes=f"Тренировка {workout_type} ({focus})"
            )

        # Питание (6-7 приемов пищи в день)
        meals_count = random.randint(6, 7)
        base_calories = 3200  # Высокие базовые калории
        calorie_increase = (current_day / total_days) * 400  # Постепенное увеличение до +400 ккал
        total_calories_target = int(base_calories + calorie_increase)
        
        meal_types = [
            'breakfast',
            'morning_snack',
            'pre_workout',
            'lunch',
            'post_workout',
            'dinner',
            'evening_snack'
        ]
        
        meal_distributions = {
            'breakfast': 0.20,         # Плотный завтрак
            'morning_snack': 0.10,
            'pre_workout': 0.15,
            'lunch': 0.20,
            'post_workout': 0.15,      # Важный прием пищи после тренировки
            'dinner': 0.15,
            'evening_snack': 0.05
        }

        protein_target = 2.2  # г на кг веса тела
        total_protein = protein_target * current_weight

        for meal_type in meal_types[:meals_count]:
            base_meal_calories = total_calories_target * meal_distributions[meal_type]
            calories = int(base_meal_calories * random.uniform(0.95, 1.15))
            
            # Распределение макронутриентов оптимизировано для набора массы
            if meal_type in ['post_workout', 'breakfast']:
                protein_ratio = 0.40  # Больше белка после тренировки и на завтрак
                fat_ratio = 0.20
                carb_ratio = 0.40
            elif meal_type == 'pre_workout':
                protein_ratio = 0.30
                fat_ratio = 0.20
                carb_ratio = 0.50  # Больше углеводов перед тренировкой
            else:
                protein_ratio = 0.35
                fat_ratio = 0.25
                carb_ratio = 0.40
            
            protein = calories * protein_ratio / 4
            fat = calories * fat_ratio / 9
            carbs = calories * carb_ratio / 4
            
            meal_time = {
                'breakfast': '07:00',
                'morning_snack': '10:00',
                'pre_workout': '12:00',
                'lunch': '14:00',
                'post_workout': '16:30',
                'dinner': '19:00',
                'evening_snack': '21:30'
            }

            Meal.objects.create(
                user=user,
                date=current_date,
                time=meal_time[meal_type],
                meal_type=meal_type,
                calories=calories,
                protein=round(protein, 1),
                fat=round(fat, 1),
                carbs=round(carbs, 1)
            )

        current_date += timedelta(days=1)
        current_day += 1

    print("Тестовые данные успешно созданы!")

if __name__ == '__main__':
    reset_database()
    create_test_data() 