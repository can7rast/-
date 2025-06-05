from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Meal, WeeklyNutritionStats, MonthlyNutritionStats
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from django.utils import timezone
from datetime import timedelta
from .forms import MealForm

class MealListView(LoginRequiredMixin, ListView):
    model = Meal
    template_name = 'nutrition/list.html'
    context_object_name = 'meals'

    def get_queryset(self):
        return Meal.objects.filter(user=self.request.user)

class MealDetailView(LoginRequiredMixin, DetailView):
    model = Meal
    template_name = 'nutrition/detail.html'
    context_object_name = 'meal'

class MealCreateView(LoginRequiredMixin, CreateView):
    model = Meal
    template_name = 'nutrition/form.html'
    fields = ['date', 'time', 'meal_type', 'calories', 'protein', 'fat', 'carbs', 'notes']
    success_url = reverse_lazy('nutrition:list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class MealUpdateView(LoginRequiredMixin, UpdateView):
    model = Meal
    template_name = 'nutrition/form.html'
    fields = ['date', 'time', 'meal_type', 'calories', 'protein', 'fat', 'carbs', 'notes']
    success_url = reverse_lazy('nutrition:list')

    def get_queryset(self):
        return Meal.objects.filter(user=self.request.user)

class MealDeleteView(LoginRequiredMixin, DeleteView):
    model = Meal
    template_name = 'nutrition/confirm_delete.html'
    success_url = reverse_lazy('nutrition:list')

    def get_queryset(self):
        return Meal.objects.filter(user=self.request.user)

def list(request):
    return HttpResponse('Заглушка для списка питания')

def add(request):
    return HttpResponse('Заглушка для добавления приема пищи')

def detail(request, pk):
    return HttpResponse(f'Заглушка для просмотра приема пищи {pk}')

def edit(request, pk):
    return HttpResponse(f'Заглушка для редактирования приема пищи {pk}')

def delete(request, pk):
    return HttpResponse(f'Заглушка для удаления приема пищи {pk}')

@login_required
def meal_list(request):
    today = timezone.now().date()
    
    # Получаем все приемы пищи пользователя
    all_meals = Meal.objects.filter(user=request.user).order_by('-date', '-time')
    
    # Получаем приемы пищи за сегодня
    today_meals = all_meals.filter(date=today)
    
    # Получаем статистику за сегодня
    today_stats = today_meals.aggregate(
        total_calories=Sum('calories'),
        total_protein=Sum('protein'),
        total_fat=Sum('fat'),
        total_carbs=Sum('carbs')
    )

    # Группируем приемы пищи по типам для текущего дня
    today_by_type = {
        'breakfast': today_meals.filter(meal_type='breakfast').first(),
        'lunch': today_meals.filter(meal_type='lunch').first(),
        'snack': today_meals.filter(meal_type='snack').first(),
        'dinner': today_meals.filter(meal_type='dinner').first(),
    }

    # Обновляем недельную и месячную статистику
    weekly_stats = WeeklyNutritionStats.calculate_for_week(request.user, today)
    monthly_stats = MonthlyNutritionStats.calculate_for_month(request.user, today)

    # Получаем статистику за предыдущие недели
    past_weeks_stats = WeeklyNutritionStats.objects.filter(
        user=request.user
    ).order_by('-week_start')[:4]  # Последние 4 недели

    # Получаем статистику за предыдущие месяцы
    past_months_stats = MonthlyNutritionStats.objects.filter(
        user=request.user
    ).order_by('-year', '-month')[:6]  # Последние 6 месяцев

    context = {
        'meals': all_meals,
        'today_meals': today_meals,
        'today_by_type': today_by_type,
        'today': today,
        'total_calories': today_stats['total_calories'] or 0,
        'total_protein': round(today_stats['total_protein'] or 0, 1),
        'total_fat': round(today_stats['total_fat'] or 0, 1),
        'total_carbs': round(today_stats['total_carbs'] or 0, 1),
        'weekly_stats': weekly_stats,
        'monthly_stats': monthly_stats,
        'past_weeks_stats': past_weeks_stats,
        'past_months_stats': past_months_stats,
    }
    return render(request, 'nutrition/list.html', context)

@login_required
def meal_detail(request, pk):
    meal = get_object_or_404(Meal, pk=pk, user=request.user)
    return render(request, 'nutrition/detail.html', {'meal': meal})

@login_required
def meal_add(request):
    if request.method == 'POST':
        form = MealForm(request.POST)
        if form.is_valid():
            meal = form.save(commit=False)
            meal.user = request.user
            meal.save()
            
            # Обновляем недельную и месячную статистику
            WeeklyNutritionStats.calculate_for_week(request.user, meal.date)
            MonthlyNutritionStats.calculate_for_month(request.user, meal.date)
            
            messages.success(request, 'Прием пищи успешно добавлен')
            return redirect('nutrition:list')
    else:
        form = MealForm(initial={'date': timezone.now().date()})
    
    return render(request, 'nutrition/form.html', {
        'form': form,
        'title': 'Добавить прием пищи'
    })

@login_required
def meal_edit(request, pk):
    meal = get_object_or_404(Meal, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = MealForm(request.POST, instance=meal)
        if form.is_valid():
            meal = form.save()
            
            # Обновляем недельную и месячную статистику
            WeeklyNutritionStats.calculate_for_week(request.user, meal.date)
            MonthlyNutritionStats.calculate_for_month(request.user, meal.date)
            
            messages.success(request, 'Прием пищи успешно обновлен')
            return redirect('nutrition:list')
    else:
        form = MealForm(instance=meal)
    
    return render(request, 'nutrition/form.html', {
        'form': form,
        'title': 'Редактировать прием пищи'
    })

@login_required
def meal_delete(request, pk):
    meal = get_object_or_404(Meal, pk=pk, user=request.user)
    meal_date = meal.date
    
    if request.method == 'POST':
        meal.delete()
        
        # Обновляем недельную и месячную статистику
        WeeklyNutritionStats.calculate_for_week(request.user, meal_date)
        MonthlyNutritionStats.calculate_for_month(request.user, meal_date)
        
        messages.success(request, 'Прием пищи успешно удален')
        return redirect('nutrition:list')
    
    return render(request, 'nutrition/delete.html', {
        'meal': meal,
        'title': 'Удалить прием пищи'
    }) 