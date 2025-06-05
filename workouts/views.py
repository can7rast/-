from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Workout
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import WorkoutForm

class WorkoutListView(LoginRequiredMixin, ListView):
    model = Workout
    template_name = 'workouts/list.html'
    context_object_name = 'workouts'

    def get_queryset(self):
        return Workout.objects.filter(user=self.request.user)

class WorkoutDetailView(LoginRequiredMixin, DetailView):
    model = Workout
    template_name = 'workouts/detail.html'
    context_object_name = 'workout'

class WorkoutCreateView(LoginRequiredMixin, CreateView):
    model = Workout
    template_name = 'workouts/form.html'
    fields = ['workout_type', 'date', 'duration', 'intensity', 'notes']
    success_url = reverse_lazy('workouts:list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class WorkoutUpdateView(LoginRequiredMixin, UpdateView):
    model = Workout
    template_name = 'workouts/form.html'
    fields = ['workout_type', 'date', 'duration', 'intensity', 'notes']
    success_url = reverse_lazy('workouts:list')

    def get_queryset(self):
        return Workout.objects.filter(user=self.request.user)

class WorkoutDeleteView(LoginRequiredMixin, DeleteView):
    model = Workout
    template_name = 'workouts/confirm_delete.html'
    success_url = reverse_lazy('workouts:list')

    def get_queryset(self):
        return Workout.objects.filter(user=self.request.user)

def list(request):
    return HttpResponse('Заглушка для списка тренировок')

def add(request):
    return HttpResponse('Заглушка для добавления тренировки')

def detail(request, pk):
    return HttpResponse(f'Заглушка для просмотра тренировки {pk}')

def edit(request, pk):
    return HttpResponse(f'Заглушка для редактирования тренировки {pk}')

def delete(request, pk):
    return HttpResponse(f'Заглушка для удаления тренировки {pk}')

@login_required
def workout_list(request):
    workouts = Workout.objects.filter(user=request.user).order_by('-date')
    return render(request, 'workouts/list.html', {'workouts': workouts})

@login_required
def workout_create(request):
    if request.method == 'POST':
        form = WorkoutForm(request.POST)
        if form.is_valid():
            workout = form.save(commit=False)
            workout.user = request.user
            workout.save()
            messages.success(request, 'Тренировка успешно добавлена!')
            return redirect('workouts:list')
    else:
        form = WorkoutForm()
    return render(request, 'workouts/form.html', {'form': form, 'title': 'Добавить тренировку'})

@login_required
def workout_detail(request, pk):
    workout = get_object_or_404(Workout, pk=pk, user=request.user)
    return render(request, 'workouts/detail.html', {
        'workout': workout,
        'duration_minutes': workout.duration
    })

@login_required
def workout_update(request, pk):
    workout = get_object_or_404(Workout, pk=pk, user=request.user)
    if request.method == 'POST':
        form = WorkoutForm(request.POST, instance=workout)
        if form.is_valid():
            form.save()
            messages.success(request, 'Тренировка успешно обновлена!')
            return redirect('workouts:list')
    else:
        form = WorkoutForm(instance=workout)
    return render(request, 'workouts/form.html', {
        'form': form,
        'title': 'Редактировать тренировку'
    })

@login_required
def workout_delete(request, pk):
    workout = get_object_or_404(Workout, pk=pk, user=request.user)
    if request.method == 'POST':
        workout.delete()
        messages.success(request, 'Тренировка успешно удалена!')
        return redirect('workouts:list')
    return render(request, 'workouts/delete.html', {'workout': workout}) 