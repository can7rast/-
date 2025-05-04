from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Sleep
from .forms import SleepForm

@login_required
def sleep_list(request):
    sleep_records = Sleep.objects.filter(user=request.user).order_by('-date')
    return render(request, 'sleep/list.html', {'sleep_records': sleep_records})

@login_required
def sleep_detail(request, pk):
    sleep = get_object_or_404(Sleep, pk=pk, user=request.user)
    return render(request, 'sleep/detail.html', {'sleep': sleep})

@login_required
def sleep_create(request):
    if request.method == 'POST':
        form = SleepForm(request.POST)
        if form.is_valid():
            sleep = form.save(commit=False)
            sleep.user = request.user
            sleep.save()
            messages.success(request, 'Запись сна успешно добавлена')
            return redirect('sleep:list')
    else:
        form = SleepForm()
    return render(request, 'sleep/form.html', {'form': form, 'title': 'Добавить запись сна'})

@login_required
def sleep_update(request, pk):
    sleep = get_object_or_404(Sleep, pk=pk, user=request.user)
    if request.method == 'POST':
        form = SleepForm(request.POST, instance=sleep)
        if form.is_valid():
            form.save()
            messages.success(request, 'Запись сна успешно обновлена')
            return redirect('sleep:list')
    else:
        form = SleepForm(instance=sleep)
    return render(request, 'sleep/form.html', {'form': form, 'title': 'Редактировать запись сна'})

@login_required
def sleep_delete(request, pk):
    sleep = get_object_or_404(Sleep, pk=pk, user=request.user)
    if request.method == 'POST':
        sleep.delete()
        messages.success(request, 'Запись сна успешно удалена')
        return redirect('sleep:list')
    return render(request, 'sleep/confirm_delete.html', {'sleep': sleep}) 