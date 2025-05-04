from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CoachAthleteForm, UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from .models import CoachAthlete
from workouts.models import Workout
from nutrition.models import Meal
from progress.models import Progress
from goals.models import Goal
from predictions.models import Prediction
from sleep.models import Sleep

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация успешно завершена!')
            return redirect('users:dashboard')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Вы успешно вошли в систему!')
            return redirect('users:dashboard')
    else:
        form = UserLoginForm()
    return render(request, 'users/login.html', {'form': form})

def user_logout(request):
    logout(request)
    messages.info(request, 'Вы вышли из системы.')
    return redirect('login')

@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Профиль успешно обновлен!')
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'users/profile.html', context)

@login_required
def athletes(request):
    if not request.user.is_coach:
        messages.error(request, 'У вас нет доступа к этой странице.')
        return redirect('users:dashboard')
    
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
        return redirect('users:dashboard')
    
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