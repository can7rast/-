import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from datetime import datetime, timedelta
from django.db.models import Sum, Count, Avg, Case, When, FloatField
from django.db import models
from workouts.models import Workout
from nutrition.models import Meal
from progress.models import Progress
from sleep.models import Sleep

class FitnessPredictor:
    def __init__(self, user):
        self.user = user
        self.model = RandomForestRegressor(
            n_estimators=200,  # Увеличиваем количество деревьев
            max_depth=10,      # Ограничиваем глубину для избежания переобучения
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=42
        )
        self.scaler = StandardScaler()
        
    def get_historical_data(self, days_back=30):
        """Получение исторических данных за указанный период"""
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=days_back)
        
        historical_progress = Progress.objects.filter(
            user=self.user,
            date__range=[start_date, end_date]
        ).order_by('date')
        
        return [{
            'date': progress.date,
            'weight': float(progress.weight),
            'confidence': 100.0  # Для исторических данных уверенность 100%
        } for progress in historical_progress]
        
    def prepare_training_data(self, days_back=90):
        """Подготовка данных для обучения модели с расширенными признаками"""
        start_date = datetime.now().date() - timedelta(days=days_back)
        
        # Получаем данные о тренировках
        workouts = Workout.objects.filter(
            user=self.user,
            date__gte=start_date
        ).values('date').annotate(
            total_duration=Sum('duration'),
            total_calories_burned=Sum('calories_burned'),
            workout_count=Count('id')
        )
        
        # Получаем данные о питании
        nutrition_data = Meal.objects.filter(
            user=self.user,
            date__gte=start_date
        ).values('date').annotate(
            calories=Sum('calories'),
            protein=Sum('protein'),
            carbs=Sum('carbs'),
            fats=Sum('fat'),
            meal_count=Count('id')
        )
        
        # Получаем данные о сне
        sleep_data = Sleep.objects.filter(
            user=self.user,
            date__gte=start_date
        ).values('date').annotate(
            sleep_duration=Avg('duration'),
            sleep_quality=Avg(
                Case(
                    When(quality='poor', then=1),
                    When(quality='fair', then=2),
                    When(quality='good', then=3),
                    When(quality='excellent', then=4),
                    default=0,
                    output_field=FloatField(),
                )
            )
        )
        
        # Получаем данные о прогрессе
        progress = Progress.objects.filter(
            user=self.user,
            date__gte=start_date
        ).values('date', 'weight', 'chest', 'waist', 'hips', 'biceps')
        
        # Преобразуем в DataFrame
        df_workouts = pd.DataFrame(workouts)
        df_nutrition = pd.DataFrame(nutrition_data)
        df_sleep = pd.DataFrame(sleep_data)
        df_progress = pd.DataFrame(progress)
        
        # Создаем базовый DataFrame с датами
        df = pd.DataFrame(index=pd.date_range(start=start_date, end=datetime.now().date()))
        
        # Объединяем все данные
        if not df_workouts.empty:
            df_workouts.set_index('date', inplace=True)
            df = df.join(df_workouts)
        
        if not df_nutrition.empty:
            df_nutrition.set_index('date', inplace=True)
            df = df.join(df_nutrition)
            
        if not df_sleep.empty:
            df_sleep.set_index('date', inplace=True)
            df = df.join(df_sleep)
            
        if not df_progress.empty:
            df_progress.set_index('date', inplace=True)
            df = df.join(df_progress)
        
        # Добавляем производные признаки
        if 'calories' in df.columns and 'protein' in df.columns:
            df['protein_ratio'] = df['protein'] * 4 / df['calories']  # Доля белка в рационе
        
        if 'total_calories_burned' in df.columns and 'calories' in df.columns:
            df['caloric_balance'] = df['calories'] - df['total_calories_burned']
        
        if 'sleep_duration' in df.columns:
            df['sleep_duration_hours'] = df['sleep_duration'].dt.total_seconds() / 3600
        
        # Добавляем скользящие средние
        if 'weight' in df.columns:
            df['weight_ma7'] = df['weight'].rolling(window=7, min_periods=1).mean()
            df['weight_ma30'] = df['weight'].rolling(window=30, min_periods=1).mean()
        
        # Заполняем пропуски
        df = df.ffill().bfill()
        
        # Добавляем временные признаки
        df['day_of_week'] = df.index.dayofweek
        df['month'] = df.index.month
        
        return df
    
    def predict_future(self, days_forward=30):
        """Прогнозирование на будущее с улучшенной оценкой уверенности"""
        # Подготавливаем исторические данные
        df = self.prepare_training_data()
        
        if df.empty or 'weight' not in df.columns:
            return None
            
        # Подготовка признаков для обучения
        feature_columns = [col for col in df.columns if col != 'weight' and not df[col].isnull().all()]
        X = df[feature_columns]
        y = df['weight']
        
        # Разделяем данные на обучающую и тестовую выборки
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)
        
        # Масштабируем признаки
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Обучаем модель
        self.model.fit(X_train_scaled, y_train)
        
        # Оцениваем качество модели
        train_score = self.model.score(X_train_scaled, y_train)
        test_score = self.model.score(X_test_scaled, y_test)
        
        # Готовим данные для прогноза
        last_data = df.iloc[-1:]
        predictions = []
        current_data = last_data.copy()
        
        for i in range(days_forward):
            # Обновляем временные признаки
            current_date = datetime.now().date() + timedelta(days=i+1)
            current_data.index = [current_date]
            current_data['day_of_week'] = current_date.weekday()
            current_data['month'] = current_date.month
            
            # Масштабируем текущие данные
            current_scaled = self.scaler.transform(current_data[feature_columns])
            
            # Получаем прогноз и доверительный интервал
            pred = self.model.predict(current_scaled)[0]
            
            # Рассчитываем уверенность на основе нескольких факторов
            days_factor = max(0, 1 - (i * 0.02))  # Уменьшение уверенности с течением времени
            quality_factor = min(train_score, test_score)
            data_quality = min(1.0, len(df) / 90)  # Фактор качества данных
            
            confidence = min(100, (days_factor * quality_factor * data_quality * 100))
            
            predictions.append({
                'date': current_date,
                'predicted_weight': float(pred),
                'confidence': float(confidence)
            })
            
            # Обновляем данные для следующего прогноза
            current_data['weight'] = pred
            if 'weight_ma7' in current_data.columns:
                current_data['weight_ma7'] = pred
            if 'weight_ma30' in current_data.columns:
                current_data['weight_ma30'] = pred
        
        return predictions
        
    def analyze_nutrition_impact(self):
        """Расширенный анализ влияния питания на прогресс"""
        df = self.prepare_training_data(days_back=30)
        if df.empty or 'weight' not in df.columns or 'calories' not in df.columns:
            return None
            
        # Анализируем разные уровни калорийности
        high_calorie_days = df[df['calories'] > 3000]
        medium_calorie_days = df[(df['calories'] >= 2000) & (df['calories'] <= 3000)]
        low_calorie_days = df[df['calories'] < 2000]
        
        # Анализируем влияние на вес с учетом тренировок
        def analyze_weight_change(data):
            if data.empty:
                return 0, 0
            
            weight_changes = data['weight'].diff()
            avg_change = weight_changes.mean()
            
            # Учитываем тренировки
            if 'total_calories_burned' in data.columns:
                workout_correlation = data['total_calories_burned'].corr(weight_changes)
            else:
                workout_correlation = 0
                
            return avg_change, abs(workout_correlation)
        
        high_change, high_confidence = analyze_weight_change(high_calorie_days)
        medium_change, medium_confidence = analyze_weight_change(medium_calorie_days)
        low_change, low_confidence = analyze_weight_change(low_calorie_days)
        
        return {
            'high_calorie_impact': high_change,
            'medium_calorie_impact': medium_change,
            'low_calorie_impact': low_change,
            'high_calorie_confidence': min(100, len(high_calorie_days) * 5 * (1 + high_confidence)),
            'medium_calorie_confidence': min(100, len(medium_calorie_days) * 5 * (1 + medium_confidence)),
            'low_calorie_confidence': min(100, len(low_calorie_days) * 5 * (1 + low_confidence))
        } 