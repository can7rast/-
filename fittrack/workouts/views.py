from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Workout, WorkoutType
from .forms import WorkoutForm, WorkoutTypeForm

@login_required
def workout_list(request):
    workouts = Workout.objects.filter(user=request.user).order_by('-date')
    return render(request, 'workouts/list.html', {'workouts': workouts})

@login_required
def workout_detail(request, pk):
    workout = get_object_or_404(Workout, pk=pk, user=request.user)
    return render(request, 'workouts/detail.html', {'workout': workout})

@login_required
def workout_create(request):
    if request.method == 'POST':
        form = WorkoutForm(request.POST)
        if form.is_valid():
            workout = form.save(commit=False)
            workout.user = request.user
            workout.save()
            messages.success(request, 'Тренировка успешно добавлена')
            return redirect('workouts:list')
    else:
        form = WorkoutForm()
    return render(request, 'workouts/form.html', {'form': form, 'title': 'Добавить тренировку'})

@login_required
def workout_update(request, pk):
    workout = get_object_or_404(Workout, pk=pk, user=request.user)
    if request.method == 'POST':
        form = WorkoutForm(request.POST, instance=workout)
        if form.is_valid():
            form.save()
            messages.success(request, 'Тренировка успешно обновлена')
            return redirect('workouts:list')
    else:
        form = WorkoutForm(instance=workout)
    return render(request, 'workouts/form.html', {'form': form, 'title': 'Редактировать тренировку'})

@login_required
def workout_delete(request, pk):
    workout = get_object_or_404(Workout, pk=pk, user=request.user)
    if request.method == 'POST':
        workout.delete()
        messages.success(request, 'Тренировка успешно удалена')
        return redirect('workouts:list')
    return render(request, 'workouts/confirm_delete.html', {'workout': workout})

@login_required
def workout_type_list(request):
    types = WorkoutType.objects.all()
    return render(request, 'workouts/type_list.html', {'types': types})

@login_required
def workout_type_create(request):
    if request.method == 'POST':
        form = WorkoutTypeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Тип тренировки успешно добавлен')
            return redirect('workouts:type_list')
    else:
        form = WorkoutTypeForm()
    return render(request, 'workouts/type_form.html', {'form': form, 'title': 'Добавить тип тренировки'})

@login_required
def workout_type_update(request, pk):
    workout_type = get_object_or_404(WorkoutType, pk=pk)
    if request.method == 'POST':
        form = WorkoutTypeForm(request.POST, instance=workout_type)
        if form.is_valid():
            form.save()
            messages.success(request, 'Тип тренировки успешно обновлен')
            return redirect('workouts:type_list')
    else:
        form = WorkoutTypeForm(instance=workout_type)
    return render(request, 'workouts/type_form.html', {'form': form, 'title': 'Редактировать тип тренировки'})

@login_required
def workout_type_delete(request, pk):
    workout_type = get_object_or_404(WorkoutType, pk=pk)
    if request.method == 'POST':
        workout_type.delete()
        messages.success(request, 'Тип тренировки успешно удален')
        return redirect('workouts:type_list')
    return render(request, 'workouts/type_confirm_delete.html', {'workout_type': workout_type}) 