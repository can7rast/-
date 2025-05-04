from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Progress, PersonalRecord
from .forms import ProgressForm, PersonalRecordForm

@login_required
def progress_list(request):
    progress_records = Progress.objects.filter(user=request.user).order_by('-date')
    personal_records = PersonalRecord.objects.filter(user=request.user).order_by('-date')
    return render(request, 'progress/list.html', {
        'progress_records': progress_records,
        'personal_records': personal_records
    })

@login_required
def progress_detail(request, pk):
    progress = get_object_or_404(Progress, pk=pk, user=request.user)
    return render(request, 'progress/detail.html', {'progress': progress})

@login_required
def progress_create(request):
    if request.method == 'POST':
        form = ProgressForm(request.POST)
        if form.is_valid():
            progress = form.save(commit=False)
            progress.user = request.user
            progress.save()
            messages.success(request, 'Запись прогресса успешно добавлена')
            return redirect('progress:list')
    else:
        form = ProgressForm()
    return render(request, 'progress/form.html', {'form': form, 'title': 'Добавить запись прогресса'})

@login_required
def progress_update(request, pk):
    progress = get_object_or_404(Progress, pk=pk, user=request.user)
    if request.method == 'POST':
        form = ProgressForm(request.POST, instance=progress)
        if form.is_valid():
            form.save()
            messages.success(request, 'Запись прогресса успешно обновлена')
            return redirect('progress:list')
    else:
        form = ProgressForm(instance=progress)
    return render(request, 'progress/form.html', {'form': form, 'title': 'Редактировать запись прогресса'})

@login_required
def progress_delete(request, pk):
    progress = get_object_or_404(Progress, pk=pk, user=request.user)
    if request.method == 'POST':
        progress.delete()
        messages.success(request, 'Запись прогресса успешно удалена')
        return redirect('progress:list')
    return render(request, 'progress/confirm_delete.html', {'progress': progress})

@login_required
def personal_record_create(request):
    if request.method == 'POST':
        form = PersonalRecordForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            record.user = request.user
            record.save()
            messages.success(request, 'Личный рекорд успешно добавлен')
            return redirect('progress:list')
    else:
        form = PersonalRecordForm()
    return render(request, 'progress/record_form.html', {'form': form, 'title': 'Добавить личный рекорд'})

@login_required
def personal_record_update(request, pk):
    record = get_object_or_404(PersonalRecord, pk=pk, user=request.user)
    if request.method == 'POST':
        form = PersonalRecordForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            messages.success(request, 'Личный рекорд успешно обновлен')
            return redirect('progress:list')
    else:
        form = PersonalRecordForm(instance=record)
    return render(request, 'progress/record_form.html', {'form': form, 'title': 'Редактировать личный рекорд'})

@login_required
def personal_record_delete(request, pk):
    record = get_object_or_404(PersonalRecord, pk=pk, user=request.user)
    if request.method == 'POST':
        record.delete()
        messages.success(request, 'Личный рекорд успешно удален')
        return redirect('progress:list')
    return render(request, 'progress/record_confirm_delete.html', {'record': record}) 