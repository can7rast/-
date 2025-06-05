from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from fittrack.workouts.models import Workout
from fittrack.nutrition.models import Meal
from fittrack.progress.models import Progress
from fittrack.sleep.models import Sleep
from django.db import models

@login_required
def dashboard(request):
    # Получаем данные за последнюю неделю
    week_ago = timezone.now() - timedelta(days=7)
    
    # Статистика тренировок
    workouts = Workout.objects.filter(
        user=request.user,
        date__gte=week_ago
    )
    workout_stats = {
        'total_workouts': workouts.count(),
        'total_duration': sum(w.duration.total_seconds() for w in workouts) / 3600,
        'avg_intensity': workouts.aggregate(avg_intensity=models.Avg('intensity'))['avg_intensity']
    }
    
    # Статистика питания
    meals = Meal.objects.filter(
        user=request.user,
        date__gte=week_ago
    )
    nutrition_stats = {
        'avg_calories': meals.aggregate(avg_calories=models.Avg('calories'))['avg_calories'] or 0,
        'avg_protein': meals.aggregate(avg_protein=models.Avg('protein'))['avg_protein'] or 0,
        'avg_fat': meals.aggregate(avg_fat=models.Avg('fat'))['avg_fat'] or 0,
        'avg_carbs': meals.aggregate(avg_carbs=models.Avg('carbs'))['avg_carbs'] or 0
    }
    
    # Статистика прогресса
    month_ago = timezone.now() - timedelta(days=30)
    progress_records = Progress.objects.filter(
        user=request.user,
        date__gte=month_ago
    ).order_by('date')
    
    if progress_records.exists():
        first_weight = progress_records.first().weight
        last_weight = progress_records.last().weight
        weight_change = last_weight - first_weight
    else:
        weight_change = 0
    
    progress_stats = {
        'weight_change': weight_change
    }
    
    # Статистика сна
    sleep_records = Sleep.objects.filter(
        user=request.user,
        date__gte=week_ago
    )
    sleep_stats = {
        'avg_duration': sleep_records.aggregate(
            avg_duration=models.Avg('duration')
        )['avg_duration'] or timedelta(hours=0),
        'avg_quality': sleep_records.aggregate(
            avg_quality=models.Avg('quality')
        )['avg_quality'] or 0
    }
    
    # Данные для графика веса
    weight_records = Progress.objects.filter(
        user=request.user
    ).order_by('date')[:30]
    
    weight_data = {
        'labels': [record.date.strftime('%d.%m') for record in weight_records],
        'values': [float(record.weight) for record in weight_records]
    }
    
    # Данные для графика тренировок
    workout_dates = Workout.objects.filter(
        user=request.user
    ).values('date__date').annotate(
        count=models.Count('id')
    ).order_by('date__date')[:30]
    
    workout_data = {
        'labels': [record['date__date'].strftime('%d.%m') for record in workout_dates],
        'values': [record['count'] for record in workout_dates]
    }
    
    # Последние тренировки
    recent_workouts = Workout.objects.filter(
        user=request.user
    ).select_related('workout_type').order_by('-date')[:5]
    
    context = {
        'workout_stats': workout_stats,
        'nutrition_stats': nutrition_stats,
        'progress_stats': progress_stats,
        'sleep_stats': sleep_stats,
        'weight_data': weight_data,
        'workout_data': workout_data,
        'recent_workouts': recent_workouts
    }
    
    return render(request, 'core/dashboard.html', context) 