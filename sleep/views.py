from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import datetime, timedelta
from .models import Sleep
from .forms import SleepForm

@login_required
def sleep_list(request):
    sleeps = Sleep.objects.filter(user=request.user).order_by('-date')
    return render(request, 'sleep/list.html', {'sleeps': sleeps})

@login_required
def sleep_create(request):
    if request.method == 'POST':
        form = SleepForm(request.POST)
        if form.is_valid():
            sleep = form.save(commit=False)
            sleep.user = request.user
            
            # Расчет длительности сна
            start_time = datetime.combine(sleep.date, sleep.start_time)
            end_time = datetime.combine(sleep.date, sleep.end_time)
            
            # Если время окончания меньше времени начала, значит сон перешел на следующий день
            if end_time < start_time:
                end_time += timedelta(days=1)
            
            duration = (end_time - start_time).total_seconds() / 3600  # конвертируем в часы
            sleep.duration = round(duration, 2)
            
            sleep.save()
            messages.success(request, 'Запись о сне успешно добавлена!')
            return redirect('sleep:list')
    else:
        form = SleepForm()
    return render(request, 'sleep/form.html', {'form': form, 'title': 'Добавить запись о сне'})

@login_required
def sleep_detail(request, pk):
    sleep = get_object_or_404(Sleep, pk=pk, user=request.user)
    return render(request, 'sleep/detail.html', {'sleep': sleep})

@login_required
def sleep_update(request, pk):
    sleep = get_object_or_404(Sleep, pk=pk, user=request.user)
    if request.method == 'POST':
        form = SleepForm(request.POST, instance=sleep)
        if form.is_valid():
            sleep = form.save(commit=False)
            
            # Расчет длительности сна
            start_time = datetime.combine(sleep.date, sleep.start_time)
            end_time = datetime.combine(sleep.date, sleep.end_time)
            
            # Если время окончания меньше времени начала, значит сон перешел на следующий день
            if end_time < start_time:
                end_time += timedelta(days=1)
            
            duration = (end_time - start_time).total_seconds() / 3600  # конвертируем в часы
            sleep.duration = round(duration, 2)
            
            sleep.save()
            messages.success(request, 'Запись о сне успешно обновлена!')
            return redirect('sleep:list')
    else:
        form = SleepForm(instance=sleep)
    return render(request, 'sleep/form.html', {'form': form, 'title': 'Редактировать запись о сне'})

@login_required
def sleep_delete(request, pk):
    sleep = get_object_or_404(Sleep, pk=pk, user=request.user)
    if request.method == 'POST':
        sleep.delete()
        messages.success(request, 'Запись о сне успешно удалена!')
        return redirect('sleep:list')
    return render(request, 'sleep/delete.html', {'sleep': sleep}) 