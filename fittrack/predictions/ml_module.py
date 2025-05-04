import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional

class FitnessPredictor:
    def __init__(self):
        self.model = LinearRegression()
        self.scaler = StandardScaler()
        self.last_training_date = None
    
    def prepare_data(self, user_data: Dict) -> Tuple[pd.DataFrame, pd.Series]:
        """Подготовка данных для обучения модели"""
        # Собираем данные из разных источников
        workouts = pd.DataFrame(user_data['workouts'])
        nutrition = pd.DataFrame(user_data['nutrition'])
        progress = pd.DataFrame(user_data['progress'])
        
        # Объединяем данные
        features = []
        target = []
        
        for i in range(len(progress) - 1):
            current_date = progress.iloc[i]['date']
            next_date = progress.iloc[i + 1]['date']
            
            # Собираем признаки
            workout_features = self._get_workout_features(workouts, current_date, next_date)
            nutrition_features = self._get_nutrition_features(nutrition, current_date, next_date)
            
            features.append({
                **workout_features,
                **nutrition_features,
                'days_between': (next_date - current_date).days
            })
            
            # Целевая переменная - изменение веса
            target.append(progress.iloc[i + 1]['weight'] - progress.iloc[i]['weight'])
        
        return pd.DataFrame(features), pd.Series(target)
    
    def _get_workout_features(self, workouts: pd.DataFrame, start_date: datetime, end_date: datetime) -> Dict:
        """Извлечение признаков из тренировок"""
        mask = (workouts['date'] >= start_date) & (workouts['date'] < end_date)
        period_workouts = workouts[mask]
        
        return {
            'total_workouts': len(period_workouts),
            'total_duration': period_workouts['duration'].sum().total_seconds() / 3600,
            'avg_intensity': period_workouts['intensity'].map({'low': 1, 'medium': 2, 'high': 3}).mean(),
            'total_calories': period_workouts['calories_burned'].sum()
        }
    
    def _get_nutrition_features(self, nutrition: pd.DataFrame, start_date: datetime, end_date: datetime) -> Dict:
        """Извлечение признаков из питания"""
        mask = (nutrition['date'] >= start_date) & (nutrition['date'] < end_date)
        period_nutrition = nutrition[mask]
        
        return {
            'avg_calories': period_nutrition['calories'].mean(),
            'avg_protein': period_nutrition['protein'].mean(),
            'avg_fat': period_nutrition['fat'].mean(),
            'avg_carbs': period_nutrition['carbs'].mean()
        }
    
    def train(self, user_data: Dict) -> None:
        """Обучение модели на данных пользователя"""
        X, y = self.prepare_data(user_data)
        
        if len(X) < 2:
            raise ValueError("Недостаточно данных для обучения")
        
        # Масштабирование признаков
        X_scaled = self.scaler.fit_transform(X)
        
        # Обучение модели
        self.model.fit(X_scaled, y)
        self.last_training_date = datetime.now()
    
    def predict(self, user_data: Dict, target_date: datetime) -> Tuple[float, float]:
        """Прогнозирование изменения веса"""
        if self.last_training_date is None:
            raise ValueError("Модель не обучена")
        
        # Подготовка данных для прогноза
        current_date = datetime.now()
        X = self._get_current_features(user_data, current_date, target_date)
        
        if X is None:
            return 0.0, 0.0
        
        # Масштабирование и прогноз
        X_scaled = self.scaler.transform([X])
        prediction = self.model.predict(X_scaled)[0]
        
        # Оценка уверенности прогноза
        confidence = self._calculate_confidence(user_data)
        
        return prediction, confidence
    
    def _get_current_features(self, user_data: Dict, current_date: datetime, target_date: datetime) -> Optional[Dict]:
        """Получение текущих признаков для прогноза"""
        try:
            workout_features = self._get_workout_features(
                pd.DataFrame(user_data['workouts']),
                current_date - timedelta(days=7),
                current_date
            )
            
            nutrition_features = self._get_nutrition_features(
                pd.DataFrame(user_data['nutrition']),
                current_date - timedelta(days=7),
                current_date
            )
            
            return {
                **workout_features,
                **nutrition_features,
                'days_between': (target_date - current_date).days
            }
        except Exception:
            return None
    
    def _calculate_confidence(self, user_data: Dict) -> float:
        """Расчет уверенности прогноза"""
        # Базовый расчет уверенности на основе количества данных
        data_points = min(
            len(user_data['workouts']),
            len(user_data['nutrition']),
            len(user_data['progress'])
        )
        
        # Нормализация уверенности от 0 до 1
        confidence = min(data_points / 30, 1.0)
        
        return confidence 