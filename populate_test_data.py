import os
import django
import random
from datetime import datetime, timedelta
import math

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fittrack.settings')
django.setup()

from django.contrib.auth import get_user_model
from workouts.models import Workout
from nutrition.models import Meal
from progress.models import Progress
from goals.models import Goal

User = get_user_model()

def create_test_data():
    # Получаем или создаем пользователя
    user, created = User.objects.get_or_create(
        username='gege',
        defaults={'email': 'gege@example.com'}
    )
    if created:
        user.set_password('gege123')
        user.save()
        print("Создан новый пользователь 'gege'")
    else:
        print("Пользователь 'gege' уже существует")

    # Удаляем старые данные
    Workout.objects.filter(user=user).delete()
    Meal.objects.filter(user=user).delete()
    Progress.objects.filter(user=user).delete()
    Goal.objects.filter(user=user).delete()

    # Устанавливаем даты
    start_date = datetime(2025, 5, 1).date()
    end_date = datetime(2025, 6, 5).date()
    current_date = start_date
    
    # Начальный вес и цель
    initial_weight = 75.0
    target_weight = 86.0
    current_weight = initial_weight

    # Создаем функцию для плавного изменения веса
    def weight_progression(day, total_days, start_weight, target_weight):
        progress = day / total_days
        # Используем синусоидальную функцию для более реалистичного прогресса
        weight_gain = (target_weight - start_weight) * (1 - math.cos(progress * math.pi)) / 2
        return start_weight + weight_gain
    
    # Создаем цель по весу (набор массы)
    Goal.objects.create(
        user=user,
        title='Набор мышечной массы',
        description='Набор массы до 86 кг с акцентом на силовые тренировки',
        goal_type='weight',
        target_value=target_weight,
        current_value=initial_weight,
        start_date=start_date,
        target_date=end_date + timedelta(days=30),
        status='active'
    )

    # Типы тренировок и их характеристики с прогрессией
    workout_types = {
        'strength': {
            'base_duration': (60, 75),  # Длительные силовые
            'progression': 1,           # +1 мин каждую тренировку
            'frequency': 0.4           # 40% всех тренировок
        },
        'cardio': {
            'base_duration': (20, 30),  # Короткие кардио для разогрева
            'progression': 0.25,        # +15 сек каждую тренировку
            'frequency': 0.2
        },
        'hiit': {
            'base_duration': (25, 35),
            'progression': 0.5,
            'frequency': 0.2
        },
        'yoga': {
            'base_duration': (40, 50),  # Для восстановления
            'progression': 0.5,
            'frequency': 0.2
        }
    }

    workout_counts = {wtype: 0 for wtype in workout_types.keys()}
    
    # Создаем записи для каждого дня
    total_days = (end_date - start_date).days
    current_day = 0

    while current_date <= end_date:
        # Прогресс
        if current_date.weekday() == 0:  # Каждый понедельник
            target_weight = weight_progression(current_day, total_days, initial_weight, target_weight)
            # Добавляем небольшую случайность
            weight_variation = random.uniform(-0.2, 0.4)  # Больше вероятность положительного отклонения
            current_weight = target_weight + weight_variation
            
            # Прогресс в измерениях тела (постепенное увеличение)
            progress_factor = 1 + (current_day / total_days) * 0.15  # максимальное увеличение на 15%
            Progress.objects.create(
                user=user,
                date=current_date,
                weight=round(current_weight, 1),
                chest=round(95 * progress_factor + random.uniform(-0.5, 0.5), 1),
                waist=round(82 * progress_factor + random.uniform(-0.5, 0.5), 1),
                hips=round(98 * progress_factor + random.uniform(-0.5, 0.5), 1),
                biceps=round(32 * progress_factor + random.uniform(-0.2, 0.2), 1)
            )

        # Тренировки (4-5 раз в неделю с акцентом на силовые)
        if current_date.weekday() in [1, 2, 4, 5] or (current_date.weekday() == 6 and random.random() < 0.7):
            # Выбираем тип тренировки с учетом частоты
            workout_type = random.choices(
                list(workout_types.keys()),
                weights=[workout_types[wt]['frequency'] for wt in workout_types.keys()]
            )[0]
            
            base_duration = workout_types[workout_type]['base_duration']
            progression = workout_types[workout_type]['progression']
            
            # Увеличиваем длительность тренировки с прогрессом
            duration = random.randint(*base_duration) + int(workout_counts[workout_type] * progression)
            duration = min(duration, 90)  # Максимум 90 минут
            
            # Интенсивность увеличивается со временем
            intensity_chance = min(0.4 + (current_day / total_days) * 0.4, 0.8)
            intensity = random.choice(['high'] if random.random() < intensity_chance else ['medium'])
            
            # Расчет сожженных калорий с учетом прогресса
            base_calories = {
                'cardio': 8,
                'strength': 7,  # Увеличенные калории для силовых
                'hiit': 10,
                'yoga': 4
            }
            intensity_multiplier = {'medium': 1.0, 'high': 1.3}  # Увеличенный множитель для высокой интенсивности
            calories_burned = int(duration * base_calories[workout_type] * intensity_multiplier[intensity])
            
            Workout.objects.create(
                user=user,
                date=current_date,
                workout_type=workout_type,
                duration=duration,
                intensity=intensity,
                calories_burned=calories_burned,
                notes=f"Тренировка {workout_type} (прогресс: {workout_counts[workout_type] + 1})"
            )
            workout_counts[workout_type] += 1

        # Питание (профицит калорий для набора массы)
        meals_count = random.randint(4, 6)  # Увеличенное количество приемов пищи
        base_calories = 3000  # Высокие базовые калории
        calorie_increase = (current_day / total_days) * 300  # Постепенное увеличение до +300 ккал
        total_calories_target = int(base_calories + calorie_increase)
        
        meal_types = ['breakfast', 'pre_workout', 'lunch', 'post_workout', 'dinner', 'snack']
        meal_distributions = {
            'breakfast': 0.2,
            'pre_workout': 0.15,
            'lunch': 0.25,
            'post_workout': 0.15,
            'dinner': 0.15,
            'snack': 0.1
        }

        for meal_type in meal_types[:meals_count]:
            base_meal_calories = total_calories_target * meal_distributions[meal_type]
            calories = int(base_meal_calories * random.uniform(0.95, 1.15))
            
            # Макронутриенты для набора массы
            protein_ratio = 0.35  # Высокий белок
            fat_ratio = 0.25
            carb_ratio = 0.40
            
            protein = calories * protein_ratio / 4
            fat = calories * fat_ratio / 9
            carbs = calories * carb_ratio / 4
            
            meal_time = {
                'breakfast': '07:30',
                'pre_workout': '10:00',
                'lunch': '13:00',
                'post_workout': '16:00',
                'dinner': '19:00',
                'snack': '21:00'
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
    create_test_data() 