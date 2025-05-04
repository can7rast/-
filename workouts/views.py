from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Workout
from django.http import HttpResponse

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