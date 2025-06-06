import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler, RobustScaler
from sklearn.model_selection import train_test_split
from datetime import datetime, timedelta
from django.db.models import Sum, Count, Avg, Case, When, FloatField
from django.db import models
from workouts.models import Workout
from nutrition.models import Meal
from progress.models import Progress
from sleep.models import Sleep
from scipy import stats

class FitnessPredictor:
    def __init__(self, user):
        self.user = user
        self.model = RandomForestRegressor(
            n_estimators=300,     # Увеличили количество деревьев
            max_depth=15,         # Увеличили глубину
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=42,
            n_jobs=-1             # Используем все доступные ядра
        )
        self.scaler = RobustScaler()  # Используем RobustScaler для лучшей обработки выбросов
        
        # Константы для проверки реалистичности прогнозов
        self.MAX_DAILY_WEIGHT_CHANGE = 0.5  # увеличили до 0.5 кг
        self.MAX_WEEKLY_WEIGHT_CHANGE = 2.0  # увеличили до 2.0 кг
        self.MIN_HEALTHY_WEIGHT = 45.0  # минимальный допустимый вес (кг)
        self.MAX_WEIGHT_CHANGE_RATE = 7.0  # увеличили до 7%
        
    def remove_outliers(self, df, column, z_threshold=3):
        """Удаление выбросов из данных"""
        if column not in df.columns:
            return df
            
        # Создаем копию DataFrame
        df_clean = df.copy()
        
        # Получаем индексы строк с выбросами
        data = df_clean[column].dropna()
        if len(data) < 2:  # Проверяем, достаточно ли данных
            return df_clean
            
        z_scores = np.abs(stats.zscore(data))
        outlier_indices = data.index[z_scores >= z_threshold]
        
        # Заменяем выбросы на NaN
        df_clean.loc[outlier_indices, column] = np.nan
        
        # Заполняем пропуски интерполяцией
        df_clean[column] = df_clean[column].interpolate(method='linear', limit_direction='both')
        
        return df_clean
        
    def get_historical_data(self, days_back=60):  # Увеличили период
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
            'confidence': 100.0
        } for progress in historical_progress]
        
    def prepare_training_data(self, days_back=180):  # Увеличили период для обучения
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
        
        # Добавляем новые производные признаки
        if 'calories' in df.columns and 'protein' in df.columns:
            df['protein_ratio'] = df['protein'] * 4 / df['calories']
            df['calories_ma7'] = df['calories'].rolling(window=7, min_periods=1).mean()
            df['calories_ma30'] = df['calories'].rolling(window=30, min_periods=1).mean()
        
        if 'total_calories_burned' in df.columns and 'calories' in df.columns:
            df['caloric_balance'] = df['calories'] - df['total_calories_burned']
            df['caloric_balance_ma7'] = df['caloric_balance'].rolling(window=7, min_periods=1).mean()
        
        if 'sleep_duration' in df.columns:
            df['sleep_duration_hours'] = df['sleep_duration']  # Просто копируем значение, оно уже в часах
            df['sleep_duration_ma7'] = df['sleep_duration_hours'].rolling(window=7, min_periods=1).mean()
        
        # Добавляем сезонные признаки
        df['season'] = df.index.month % 12 // 3  # 0-весна, 1-лето, 2-осень, 3-зима
        df['day_of_year'] = df.index.dayofyear
        df['week_of_year'] = df.index.isocalendar().week
        
        # Добавляем нелинейные признаки
        if 'weight' in df.columns:
            df['weight_ma7'] = df['weight'].rolling(window=7, min_periods=1).mean()
            df['weight_ma30'] = df['weight'].rolling(window=30, min_periods=1).mean()
            df['weight_trend'] = df['weight'].diff().rolling(window=7).mean()
            df['weight_momentum'] = df['weight'].diff().diff().rolling(window=7).mean()
        
        # Заполняем пропуски более продвинутым способом
        numeric_columns = df.select_dtypes(include=[np.number]).columns
        for col in numeric_columns:
            if df[col].isnull().any():
                # Используем скользящее среднее для заполнения пропусков
                df[col] = df[col].fillna(df[col].rolling(window=7, min_periods=1, center=True).mean())
                # Используем интерполяцию
                df[col] = df[col].interpolate(method='linear', limit_direction='both')
                # Используем прямое и обратное заполнение без устаревшего метода
                df[col] = df[col].ffill().bfill()
        
        # Удаляем выбросы после заполнения пропусков
        df = self.remove_outliers(df, 'weight')
        if 'calories' in df.columns:
            df = self.remove_outliers(df, 'calories')
        
        return df
    
    def is_prediction_realistic(self, current_weight, predicted_weight, days_passed):
        """Проверка реалистичности прогноза"""
        if predicted_weight < self.MIN_HEALTHY_WEIGHT:
            return False
            
        daily_change = abs(predicted_weight - current_weight) / max(1, days_passed)
        weekly_change = daily_change * 7
        percent_change = abs(predicted_weight - current_weight) / current_weight * 100
        
        # Смягчаем условия для коротких периодов
        if days_passed <= 7:
            if daily_change > self.MAX_DAILY_WEIGHT_CHANGE * 1.2:  # Даем 20% запаса
                return False
        else:
            if daily_change > self.MAX_DAILY_WEIGHT_CHANGE:
                return False
                
        if weekly_change > self.MAX_WEEKLY_WEIGHT_CHANGE:
            return False
            
        if percent_change > self.MAX_WEIGHT_CHANGE_RATE:
            return False
            
        return True
        
    def adjust_prediction(self, current_weight, predicted_weight, days_passed):
        """Корректировка прогноза в допустимые пределы"""
        if self.is_prediction_realistic(current_weight, predicted_weight, days_passed):
            return predicted_weight
            
        # Ограничиваем изменение веса максимально допустимым
        max_change = min(
            self.MAX_DAILY_WEIGHT_CHANGE * days_passed,
            self.MAX_WEEKLY_WEIGHT_CHANGE * (days_passed / 7),
            current_weight * (self.MAX_WEIGHT_CHANGE_RATE / 100)
        )
        
        if predicted_weight > current_weight:
            return min(current_weight + max_change, predicted_weight)
        else:
            return max(current_weight - max_change, predicted_weight)
            
    def calculate_confidence(self, current_weight, predicted_weight, days_passed, base_confidence):
        """Расчет уверенности в прогнозе"""
        # Начинаем с базовой уверенности
        confidence = base_confidence
        
        # Рассчитываем факторы уверенности
        daily_change = abs(predicted_weight - current_weight) / max(1, days_passed)
        
        # Фактор времени (уменьшается с увеличением периода прогноза)
        time_factor = np.exp(-0.005 * days_passed)  # Сделали более плавным
        
        # Фактор изменения веса
        change_factor = 1.0
        if daily_change > 0:
            change_factor = max(0.3, 1.0 - (daily_change / self.MAX_DAILY_WEIGHT_CHANGE))
        
        # Исторический фактор
        historical_changes = self.get_historical_weight_changes()
        if historical_changes:
            avg_historical_change = np.mean(historical_changes)
            if avg_historical_change > 0:
                historical_factor = max(0.5, 1.0 - abs(daily_change - avg_historical_change) / avg_historical_change)
            else:
                historical_factor = 0.7
        else:
            historical_factor = 0.7
        
        # Комбинируем все факторы
        confidence = confidence * time_factor * change_factor * historical_factor
        
        # Если прогноз нереалистичен, значительно снижаем уверенность, но не до нуля
        if not self.is_prediction_realistic(current_weight, predicted_weight, days_passed):
            confidence *= 0.3
        
        # Гарантируем минимальный уровень уверенности
        return max(10.0, min(100.0, confidence))
        
    def get_historical_weight_changes(self):
        """Получение истории изменений веса"""
        progress_records = Progress.objects.filter(
            user=self.user
        ).order_by('date').values('weight', 'date')
        
        if len(progress_records) < 2:
            return []
            
        changes = []
        for i in range(1, len(progress_records)):
            days = (progress_records[i]['date'] - progress_records[i-1]['date']).days
            if days > 0:
                daily_change = abs(progress_records[i]['weight'] - progress_records[i-1]['weight']) / days
                changes.append(daily_change)
                
        return changes
        
    def analyze_caloric_trend(self, days_back=30):
        """Анализ тренда калорийности за последний месяц"""
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=days_back)
        
        # Получаем данные о питании
        meals = Meal.objects.filter(
            user=self.user,
            date__range=[start_date, end_date]
        ).values('date').annotate(
            daily_calories=Sum('calories')
        ).order_by('date')
        
        if not meals:
            return None, 0
            
        # Считаем среднюю калорийность
        total_calories = sum(meal['daily_calories'] or 0 for meal in meals)
        days_with_data = len(meals)
        
        if days_with_data == 0:
            return None, 0
            
        avg_calories = total_calories / days_with_data
        
        # Определяем тренд
        if avg_calories >= 3000:
            return 'bulk', avg_calories  # набор массы
        else:
            return 'cut', avg_calories   # снижение веса
            
    def adjust_prediction_by_calories(self, current_weight, predicted_weight, caloric_trend, avg_calories):
        """Корректировка прогноза на основе тренда калорийности"""
        if caloric_trend is None:
            return predicted_weight
            
        # Рассчитываем ожидаемое изменение веса на основе калорийности
        # 7700 ккал = 1 кг жира
        daily_caloric_difference = avg_calories - 2500  # 2500 - примерная норма
        weekly_weight_change = (daily_caloric_difference * 7) / 7700
        
        if caloric_trend == 'bulk':
            # При профиците калорий вес должен расти
            if predicted_weight <= current_weight:
                # Корректируем прогноз в сторону увеличения
                adjusted_weight = current_weight + (weekly_weight_change * 0.7)  # 70% от теоретического изменения
                return max(predicted_weight, adjusted_weight)
        else:
            # При дефиците калорий вес должен снижаться
            if predicted_weight >= current_weight:
                # Корректируем прогноз в сторону уменьшения
                adjusted_weight = current_weight + (weekly_weight_change * 0.7)  # 70% от теоретического изменения
                return min(predicted_weight, adjusted_weight)
                
        return predicted_weight
        
    def predict_future(self, days_forward=60):
        """Прогнозирование на будущее с учетом калорийности"""
        df = self.prepare_training_data()
        
        if df.empty or 'weight' not in df.columns:
            return None
            
        # Анализируем тренд калорийности
        caloric_trend, avg_calories = self.analyze_caloric_trend()
        
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
        
        # Увеличиваем базовую уверенность
        base_confidence = max(50.0, min(100.0, (train_score + test_score) / 2 * 150))
        
        # Готовим данные для прогноза
        last_data = df.iloc[-1:]
        current_weight = float(last_data['weight'].iloc[0])
        predictions = []
        current_data = last_data.copy()
        
        for i in range(days_forward):
            current_date = datetime.now().date() + timedelta(days=i+1)
            current_data.index = [current_date]
            
            # Обновляем временные признаки
            current_data['day_of_week'] = current_date.weekday()
            current_data['month'] = current_date.month
            current_data['season'] = current_date.month % 12 // 3
            current_data['day_of_year'] = current_date.timetuple().tm_yday
            current_data['week_of_year'] = datetime.isocalendar(current_date).week
            
            # Масштабируем текущие данные
            current_scaled = self.scaler.transform(current_data[feature_columns])
            
            # Получаем прогноз
            raw_pred = self.model.predict(current_scaled)[0]
            
            # Корректируем прогноз с учетом ограничений
            adjusted_pred = self.adjust_prediction(current_weight, raw_pred, i + 1)
            
            # Корректируем прогноз с учетом калорийности
            final_pred = self.adjust_prediction_by_calories(current_weight, adjusted_pred, caloric_trend, avg_calories)
            
            # Получаем уверенность
            confidence = self.calculate_confidence(
                current_weight,
                final_pred,
                i + 1,
                base_confidence
            )
            
            # Добавляем информацию о тренде
            prediction_info = {
                'date': current_date,
                'predicted_weight': float(final_pred),
                'confidence': float(confidence),
                'trend': caloric_trend,
                'avg_calories': float(avg_calories) if avg_calories else 0
            }
            
            predictions.append(prediction_info)
            
            # Обновляем текущий вес для следующей итерации
            current_weight = final_pred
            current_data['weight'] = final_pred
            
            # Обновляем производные признаки
            if 'weight_ma7' in current_data.columns:
                current_data['weight_ma7'] = final_pred
            if 'weight_ma30' in current_data.columns:
                current_data['weight_ma30'] = final_pred
            if 'weight_trend' in current_data.columns:
                current_data['weight_trend'] = 0
            if 'weight_momentum' in current_data.columns:
                current_data['weight_momentum'] = 0
        
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