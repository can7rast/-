from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import datetime, timedelta
import random
from nutrition.models import Meal

User = get_user_model()

class Command(BaseCommand):
    help = 'Заполняет базу данных тестовыми данными о питании'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='Имя пользователя')

    def handle(self, *args, **options):
        try:
            user = User.objects.get(username=options['username'])
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Пользователь {options["username"]} не найден'))
            return

        # Определяем период
        start_date = datetime(2025, 5, 1).date()
        end_date = datetime(2025, 6, 5).date()
        
        # Типичные приемы пищи
        meal_patterns = {
            'breakfast': {
                'time_range': ('07:00', '10:00'),
                'calories': (300, 600),
                'protein': (15, 30),
                'fat': (10, 20),
                'carbs': (30, 60),
                'probability': 0.9  # вероятность наличия завтрака
            },
            'lunch': {
                'time_range': ('12:00', '15:00'),
                'calories': (500, 800),
                'protein': (25, 40),
                'fat': (15, 25),
                'carbs': (50, 80),
                'probability': 0.95
            },
            'snack': {
                'time_range': ('15:30', '17:30'),
                'calories': (200, 400),
                'protein': (5, 15),
                'fat': (5, 15),
                'carbs': (20, 40),
                'probability': 0.7
            },
            'dinner': {
                'time_range': ('18:00', '21:00'),
                'calories': (400, 700),
                'protein': (20, 35),
                'fat': (15, 25),
                'carbs': (40, 70),
                'probability': 0.85
            }
        }

        def random_time(time_range):
            start = datetime.strptime(time_range[0], '%H:%M')
            end = datetime.strptime(time_range[1], '%H:%M')
            time_diff = (end - start).seconds
            random_seconds = random.randint(0, time_diff)
            return (start + timedelta(seconds=random_seconds)).time()

        # Удаляем существующие записи за этот период
        Meal.objects.filter(
            user=user,
            date__range=(start_date, end_date)
        ).delete()

        # Создаем записи
        current_date = start_date
        meals_created = 0

        while current_date <= end_date:
            # В выходные дни (суббота и воскресенье) немного другие паттерны
            is_weekend = current_date.weekday() >= 5
            
            for meal_type, pattern in meal_patterns.items():
                # Корректируем вероятность для выходных
                probability = pattern['probability']
                if is_weekend:
                    if meal_type == 'breakfast':
                        probability = 0.7  # люди часто пропускают завтрак в выходные
                    elif meal_type == 'lunch':
                        probability = 0.8  # обед может быть позже
                    elif meal_type == 'dinner':
                        probability = 0.95  # ужин чаще в выходные

                if random.random() < probability:
                    # Создаем прием пищи
                    meal = Meal(
                        user=user,
                        date=current_date,
                        time=random_time(pattern['time_range']),
                        meal_type=meal_type,
                        calories=random.randint(*pattern['calories']),
                        protein=round(random.uniform(*pattern['protein']), 1),
                        fat=round(random.uniform(*pattern['fat']), 1),
                        carbs=round(random.uniform(*pattern['carbs']), 1),
                        notes=''
                    )
                    meal.save()
                    meals_created += 1

            current_date += timedelta(days=1)

        self.stdout.write(
            self.style.SUCCESS(
                f'Успешно создано {meals_created} записей о приемах пищи '
                f'за период с {start_date} по {end_date}'
            )
        ) 