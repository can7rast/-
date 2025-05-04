from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Goal
from .forms import GoalForm

@login_required
def goal_list(request):
    goals = Goal.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'goals/list.html', {'goals': goals})

@login_required
def goal_detail(request, pk):
    goal = get_object_or_404(Goal, pk=pk, user=request.user)
    return render(request, 'goals/detail.html', {'goal': goal})

@login_required
def goal_create(request):
    if request.method == 'POST':
        form = GoalForm(request.POST)
        if form.is_valid():
            goal = form.save(commit=False)
            goal.user = request.user
            goal.save()
            messages.success(request, 'Цель успешно добавлена')
            return redirect('goals:list')
    else:
        form = GoalForm()
    return render(request, 'goals/form.html', {'form': form, 'title': 'Добавить цель'})

@login_required
def goal_update(request, pk):
    goal = get_object_or_404(Goal, pk=pk, user=request.user)
    if request.method == 'POST':
        form = GoalForm(request.POST, instance=goal)
        if form.is_valid():
            form.save()
            messages.success(request, 'Цель успешно обновлена')
            return redirect('goals:list')
    else:
        form = GoalForm(instance=goal)
    return render(request, 'goals/form.html', {'form': form, 'title': 'Редактировать цель'})

@login_required
def goal_delete(request, pk):
    goal = get_object_or_404(Goal, pk=pk, user=request.user)
    if request.method == 'POST':
        goal.delete()
        messages.success(request, 'Цель успешно удалена')
        return redirect('goals:list')
    return render(request, 'goals/confirm_delete.html', {'goal': goal}) 