import os
import django
import random

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fittrack.settings')
django.setup()

from django.contrib.auth import get_user_model
from workouts.models import Workout

User = get_user_model()

def update_workouts():
    try:
        # Получаем пользователя
        user = User.objects.get(username='gege')
        
        # Получаем все тренировки пользователя
        workouts = Workout.objects.filter(user=user)
        
        # Правильные типы тренировок из модели
        workout_types = ['cardio', 'strength', 'hiit', 'yoga', 'stretching', 'other']
        
        # Словарь для замены старых типов на новые
        type_mapping = {
            'running': 'cardio',
            'cycling': 'cardio',
            'swimming': 'cardio',
            'gym': 'strength',
            # Остальные типы будут заменены случайным образом
        }
        
        print(f"Найдено {workouts.count()} тренировок для обновления...")
        
        # Обновляем каждую тренировку
        for workout in workouts:
            old_type = workout.workout_type
            
            # Если есть прямое соответствие в маппинге, используем его
            if old_type in type_mapping:
                new_type = type_mapping[old_type]
            # Если тип уже правильный, оставляем его
            elif old_type in workout_types:
                new_type = old_type
            # Иначе выбираем случайный тип
            else:
                new_type = random.choice(workout_types)
            
            # Обновляем тип тренировки
            workout.workout_type = new_type
            workout.save()
            
            print(f"Обновлена тренировка от {workout.date}: {old_type} -> {new_type}")
        
        print("\nВсе тренировки успешно обновлены!")
        
    except User.DoesNotExist:
        print("Пользователь 'gege' не найден!")
        return

if __name__ == '__main__':
    update_workouts() 