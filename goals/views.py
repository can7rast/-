from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Goal
from .forms import GoalForm

@login_required
def goal_list(request):
    """Отображает список целей пользователя"""
    goals = Goal.objects.filter(user=request.user)
    context = {'goals': goals}
    return render(request, 'goals/goal_list.html', context)

@login_required
def add_goal(request):
    """Добавляет новую цель"""
    if request.method != 'POST':
        form = GoalForm()
    else:
        form = GoalForm(data=request.POST)
        if form.is_valid():
            new_goal = form.save(commit=False)
            new_goal.user = request.user
            new_goal.save()
            messages.success(request, 'Цель успешно добавлена!')
            return redirect('goals:list')
    
    context = {'form': form}
    return render(request, 'goals/goal_form.html', context)

@login_required
def goal_detail(request, goal_id):
    """Отображает детали цели"""
    goal = get_object_or_404(Goal, id=goal_id, user=request.user)
    context = {'goal': goal}
    return render(request, 'goals/goal_detail.html', context)

@login_required
def edit_goal(request, goal_id):
    """Редактирует существующую цель"""
    goal = get_object_or_404(Goal, id=goal_id, user=request.user)
    
    if request.method != 'POST':
        form = GoalForm(instance=goal)
    else:
        form = GoalForm(instance=goal, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Цель успешно обновлена!')
            return redirect('goals:detail', goal_id=goal.id)
    
    context = {'goal': goal, 'form': form}
    return render(request, 'goals/goal_form.html', context)

@login_required
def delete_goal(request, goal_id):
    """Удаляет цель"""
    goal = get_object_or_404(Goal, id=goal_id, user=request.user)
    
    if request.method == 'POST':
        goal.delete()
        messages.success(request, 'Цель успешно удалена!')
        return redirect('goals:list')
    
    context = {'goal': goal}
    return render(request, 'goals/goal_confirm_delete.html', context)

@login_required
def update_goal_status(request, goal_id):
    """Обновляет статус цели"""
    goal = get_object_or_404(Goal, id=goal_id, user=request.user)
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Goal.STATUS_CHOICES):
            goal.status = new_status
            goal.save()
            messages.success(request, 'Статус цели успешно обновлен!')
        else:
            messages.error(request, 'Некорректный статус!')
    
    return redirect('goals:detail', goal_id=goal.id) 