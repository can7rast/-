from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Meal
from django.http import HttpResponse

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