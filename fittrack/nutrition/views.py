from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Meal
from .forms import MealForm

@login_required
def meal_list(request):
    meals = Meal.objects.filter(user=request.user).order_by('-date', '-time')
    return render(request, 'nutrition/list.html', {'meals': meals})

@login_required
def meal_detail(request, pk):
    meal = get_object_or_404(Meal, pk=pk, user=request.user)
    return render(request, 'nutrition/detail.html', {'meal': meal})

@login_required
def meal_create(request):
    if request.method == 'POST':
        form = MealForm(request.POST)
        if form.is_valid():
            meal = form.save(commit=False)
            meal.user = request.user
            meal.save()
            messages.success(request, 'Прием пищи успешно добавлен')
            return redirect('nutrition:list')
    else:
        form = MealForm()
    return render(request, 'nutrition/form.html', {'form': form, 'title': 'Добавить прием пищи'})

@login_required
def meal_update(request, pk):
    meal = get_object_or_404(Meal, pk=pk, user=request.user)
    if request.method == 'POST':
        form = MealForm(request.POST, instance=meal)
        if form.is_valid():
            form.save()
            messages.success(request, 'Прием пищи успешно обновлен')
            return redirect('nutrition:list')
    else:
        form = MealForm(instance=meal)
    return render(request, 'nutrition/form.html', {'form': form, 'title': 'Редактировать прием пищи'})

@login_required
def meal_delete(request, pk):
    meal = get_object_or_404(Meal, pk=pk, user=request.user)
    if request.method == 'POST':
        meal.delete()
        messages.success(request, 'Прием пищи успешно удален')
        return redirect('nutrition:list')
    return render(request, 'nutrition/confirm_delete.html', {'meal': meal}) 