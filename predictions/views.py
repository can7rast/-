from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Prediction
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .ml_model import FitnessPredictor
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
from django.db.models import Avg, Count, Sum
from goals.models import Goal
from workouts.models import Workout
from nutrition.models import Meal
from progress.models import Progress
from plotly.subplots import make_subplots

class PredictionListView(LoginRequiredMixin, ListView):
    model = Prediction
    template_name = 'predictions/list.html'
    context_object_name = 'predictions'

    def get_queryset(self):
        return Prediction.objects.filter(user=self.request.user)

class PredictionDetailView(LoginRequiredMixin, DetailView):
    model = Prediction
    template_name = 'predictions/detail.html'
    context_object_name = 'prediction'

class PredictionCreateView(LoginRequiredMixin, CreateView):
    model = Prediction
    template_name = 'predictions/form.html'
    fields = ['prediction_type', 'current_value', 'predicted_value', 'prediction_date', 'target_date', 'confidence', 'notes']
    success_url = reverse_lazy('predictions:list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class PredictionUpdateView(LoginRequiredMixin, UpdateView):
    model = Prediction
    template_name = 'predictions/form.html'
    fields = ['prediction_type', 'current_value', 'predicted_value', 'prediction_date', 'target_date', 'confidence', 'notes']
    success_url = reverse_lazy('predictions:list')

    def get_queryset(self):
        return Prediction.objects.filter(user=self.request.user)

class PredictionDeleteView(LoginRequiredMixin, DeleteView):
    model = Prediction
    template_name = 'predictions/confirm_delete.html'
    success_url = reverse_lazy('predictions:list')

    def get_queryset(self):
        return Prediction.objects.filter(user=self.request.user)

def list(request):
    return HttpResponse('Заглушка для списка прогнозов')

def add(request):
    return HttpResponse('Заглушка для добавления прогноза')

def detail(request, pk):
    return HttpResponse(f'Заглушка для просмотра прогноза {pk}')

def edit(request, pk):
    return HttpResponse(f'Заглушка для редактирования прогноза {pk}')

def delete(request, pk):
    return HttpResponse(f'Заглушка для удаления прогноза {pk}')

@login_required
def index(request):
    """Главная страница прогнозов с аналитикой"""
    predictor = FitnessPredictor(request.user)
    
    # Получаем текущие показатели
    latest_progress = Progress.objects.filter(user=request.user).order_by('-date').first()
    current_weight = latest_progress.weight if latest_progress else 0
    
    # Средние калории за последние 30 дней
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=30)
    avg_calories = Meal.objects.filter(
        user=request.user,
        date__range=[start_date, end_date]
    ).values('date').annotate(
        daily_calories=Sum('calories')
    ).aggregate(Avg('daily_calories'))['daily_calories__avg'] or 0
    
    # Количество тренировок за последнюю неделю
    week_start = end_date - timedelta(days=end_date.weekday())
    workouts_per_week = Workout.objects.filter(
        user=request.user,
        date__range=[week_start, end_date]
    ).count()
    
    # Получаем исторические данные за последний месяц
    historical_data = predictor.get_historical_data(days_back=30)
    
    # Получаем прогнозы на следующий месяц
    future_predictions = predictor.predict_future(days_forward=30)
    
    if future_predictions:
        predicted_weight = future_predictions[-1]['predicted_weight']
        
        # Объединяем исторические данные и прогнозы для графика
        all_data = historical_data + future_predictions
        
        # Создаем график с двумя наборами данных
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        
        # Разделяем данные на исторические и прогнозируемые
        historical_dates = [d['date'].strftime('%d.%m.%Y') for d in historical_data]
        historical_weights = [d['weight'] for d in historical_data]
        
        future_dates = [d['date'].strftime('%d.%m.%Y') for d in future_predictions]
        future_weights = [d['predicted_weight'] for d in future_predictions]
        confidence = [d['confidence'] for d in future_predictions]
        
        # Добавляем линию исторических данных
        fig.add_trace(
            go.Scatter(
                x=historical_dates,
                y=historical_weights,
                name="Исторические данные",
                line=dict(color="blue"),
                mode='lines+markers'
            ),
            secondary_y=False
        )
        
        # Добавляем линию прогноза
        fig.add_trace(
            go.Scatter(
                x=future_dates,
                y=future_weights,
                name="Прогноз",
                line=dict(color="green", dash='dot'),
                mode='lines+markers'
            ),
            secondary_y=False
        )
        
        # Добавляем линию уверенности
        fig.add_trace(
            go.Scatter(
                x=future_dates,
                y=confidence,
                name="Уверенность прогноза",
                line=dict(color="red", dash='dot'),
                mode='lines'
            ),
            secondary_y=True
        )
        
        # Обновляем макет
        fig.update_layout(
            title='Динамика веса и прогноз',
            xaxis_title='Дата',
            template='plotly_white',
            height=500,
            hovermode='x unified'
        )
        
        # Обновляем оси Y
        fig.update_yaxes(title_text="Вес (кг)", secondary_y=False)
        fig.update_yaxes(title_text="Уверенность (%)", secondary_y=True)
        
        # Получаем активную цель
        goal = Goal.objects.filter(user=request.user, status='active').first()
        if goal and goal.target_value:
            days_to_goal = (goal.target_date - datetime.now().date()).days
            current_value = float(goal.current_value)
            target_value = float(goal.target_value)
            progress_percentage = min(100, max(0, (
                (current_weight - current_value) / 
                (target_value - current_value)
            ) * 100))
        else:
            days_to_goal = None
            progress_percentage = None
        
        # Анализируем влияние питания
        nutrition_impact = predictor.analyze_nutrition_impact()
        
        # Формируем рекомендации на основе анализа данных
        recommendations = []
        if nutrition_impact:
            if nutrition_impact['high_calorie_impact'] > 0:
                recommendations.append("Высококалорийные дни положительно влияют на набор массы")
            if nutrition_impact['low_calorie_impact'] < 0:
                recommendations.append("В дни с низкой калорийностью наблюдается потеря веса")
        
        # Берем только первую неделю прогнозов для детального анализа
        weekly_predictions = []
        prev_weight = current_weight
        for pred in future_predictions[:7]:
            weight_change = pred['predicted_weight'] - prev_weight
            
            if abs(weight_change) < 0.1:
                recommendation = "Вес стабилен, продолжайте в том же духе"
            elif weight_change > 0:
                recommendation = "Прогресс в наборе массы, поддерживайте режим"
            else:
                recommendation = "Рекомендуется увеличить калорийность"
            
            pred['weight_change'] = weight_change
            pred['recommendation'] = recommendation
            weekly_predictions.append(pred)
            prev_weight = pred['predicted_weight']
        
        context = {
            'current_weight': current_weight,
            'avg_calories': avg_calories,
            'workouts_per_week': workouts_per_week,
            'predicted_weight': predicted_weight,
            'weight_plot': fig.to_html(),
            'predictions': weekly_predictions,
            'nutrition_impact': nutrition_impact,
            'recommendations': recommendations,
            'progress_percentage': progress_percentage,
            'days_to_goal': days_to_goal
        }
    else:
        context = {
            'error': 'Недостаточно данных для построения прогноза'
        }
    
    return render(request, 'predictions/index.html', context)

@login_required
def prediction_list(request):
    """Список всех прогнозов"""
    predictions = Prediction.objects.filter(user=request.user).order_by('-prediction_date')
    return render(request, 'predictions/list.html', {'predictions': predictions})

@login_required
def create_prediction(request):
    """Создание нового прогноза"""
    if request.method == 'POST':
        # Здесь будет логика создания прогноза
        return redirect('predictions:list')
    return render(request, 'predictions/form.html')

@login_required
def get_prediction_data(request):
    """API endpoint для получения данных прогноза"""
    predictor = FitnessPredictor(request.user)
    predictions = predictor.predict_future(days_forward=30)
    nutrition_impact = predictor.analyze_nutrition_impact()
    
    if predictions and nutrition_impact:
        return JsonResponse({
            'predictions': predictions,
            'nutrition_impact': nutrition_impact
        })
    
    return JsonResponse({'error': 'Недостаточно данных для прогноза'}, status=400) 