from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from .forms import CoachAthleteForm, UserRegisterForm, UserUpdateForm, ProfileUpdateForm, UserLoginForm
from .models import CoachAthlete, Profile
from workouts.models import Workout
from nutrition.models import Meal
from progress.models import Progress
from predictions.models import Prediction
from sleep.models import Sleep
from goals.models import Goal
from django.db import models

def register(request):
    """Регистрация нового пользователя"""
    if request.method != 'POST':
        form = UserRegisterForm()
    else:
        form = UserRegisterForm(data=request.POST)
        
        if form.is_valid():
            new_user = form.save()
            login(request, new_user)
            messages.success(request, 'Вы успешно зарегистрировались!')
            return redirect('users:profile')
            
    context = {'form': form}
    return render(request, 'users/register.html', context)

def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Вы успешно вошли в систему!')
                return redirect('users:dashboard')
        messages.error(request, 'Нет пользователя с такими данными')
    else:
        form = UserLoginForm()
    return render(request, 'users/login.html', {'form': form})

def user_logout(request):
    logout(request)
    messages.info(request, 'Вы вышли из системы.')
    return redirect('login')

@login_required
def profile(request):
    """Отображает профиль пользователя с основной статистикой"""
    today = timezone.now().date()
    week_ago = today - timedelta(days=7)
    
    # Получаем статистику по тренировкам
    total_workouts = Workout.objects.filter(user=request.user).count()
    recent_workouts = Workout.objects.filter(
        user=request.user,
        date__gte=week_ago
    ).order_by('-date')[:5]
    
    # Подсчитываем общее количество сожженных калорий
    total_calories_burned = Workout.objects.filter(
        user=request.user
    ).aggregate(total=models.Sum('calories_burned'))['total'] or 0
    
    # Получаем активные цели
    active_goals_list = Goal.objects.filter(
        user=request.user,
        status='active'
    ).order_by('target_date')[:4]
    active_goals = active_goals_list.count()
    
    # Подсчитываем серию тренировок
    workout_streak = calculate_workout_streak(request.user)
    
    context = {
        'recent_workouts': recent_workouts,
        'total_workouts': total_workouts,
        'total_calories_burned': total_calories_burned,
        'active_goals': active_goals,
        'active_goals_list': active_goals_list,
        'workout_streak': workout_streak,
    }
    
    return render(request, 'users/profile.html', context)

def calculate_workout_streak(user):
    """Подсчитывает текущую серию тренировок"""
    today = timezone.now().date()
    workouts = Workout.objects.filter(
        user=user,
        date__lte=today
    ).order_by('-date')
    
    if not workouts:
        return 0
    
    streak = 0
    last_date = today
    
    for workout in workouts:
        if (last_date - workout.date).days <= 1:
            streak += 1
            last_date = workout.date
        else:
            break
    
    return streak

@login_required
def edit_profile(request):
    """Редактирование профиля пользователя"""
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Профиль успешно обновлен!')
            return redirect('users:profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'users/edit_profile.html', context)

@login_required
def athletes(request):
    if not request.user.is_coach:
        messages.error(request, 'У вас нет доступа к этой странице.')
        return redirect('dashboard')
    
    athletes = CoachAthlete.objects.filter(coach=request.user)
    form = CoachAthleteForm(coach=request.user)
    
    if request.method == 'POST':
        form = CoachAthleteForm(request.user, request.POST)
        if form.is_valid():
            coach_athlete = form.save(commit=False)
            coach_athlete.coach = request.user
            coach_athlete.save()
            messages.success(request, 'Спортсмен успешно добавлен!')
            return redirect('users:athletes')
    
    context = {
        'athletes': athletes,
        'form': form
    }
    return render(request, 'users/athletes.html', context)

@login_required
def remove_athlete(request, athlete_id):
    if not request.user.is_coach:
        messages.error(request, 'У вас нет доступа к этой странице.')
        return redirect('dashboard')
    
    try:
        coach_athlete = CoachAthlete.objects.get(coach=request.user, athlete_id=athlete_id)
        coach_athlete.delete()
        messages.success(request, 'Спортсмен успешно удален из вашего списка.')
    except CoachAthlete.DoesNotExist:
        messages.error(request, 'Спортсмен не найден.')
    
    return redirect('users:athletes')

@login_required
def dashboard(request):
    last_workout = Workout.objects.filter(user=request.user).order_by('-date').first()
    last_meal = Meal.objects.filter(user=request.user).order_by('-date', '-time').first()
    last_progress = Progress.objects.filter(user=request.user).order_by('-date').first()
    active_goals_count = Goal.objects.filter(user=request.user, status='active').count()
    last_prediction = Prediction.objects.filter(user=request.user).order_by('-prediction_date').first()
    last_sleep = Sleep.objects.filter(user=request.user).order_by('-date').first()

    context = {
        'last_workout': last_workout,
        'last_meal': last_meal,
        'last_progress': last_progress,
        'active_goals_count': active_goals_count,
        'last_prediction': last_prediction,
        'last_sleep': last_sleep,
    }
    return render(request, 'users/dashboard.html', context)

def add_athlete(request):
    return render(request, 'users/add_athlete.html') 