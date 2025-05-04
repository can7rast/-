from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Goal
from django.http import HttpResponse

class GoalListView(LoginRequiredMixin, ListView):
    model = Goal
    template_name = 'goals/list.html'
    context_object_name = 'goals'

    def get_queryset(self):
        return Goal.objects.filter(user=self.request.user)

class GoalDetailView(LoginRequiredMixin, DetailView):
    model = Goal
    template_name = 'goals/detail.html'
    context_object_name = 'goal'

class GoalCreateView(LoginRequiredMixin, CreateView):
    model = Goal
    template_name = 'goals/form.html'
    fields = ['goal_type', 'current_value', 'target_value', 'start_date', 'end_date', 'status', 'description', 'notes']
    success_url = reverse_lazy('goals:list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class GoalUpdateView(LoginRequiredMixin, UpdateView):
    model = Goal
    template_name = 'goals/form.html'
    fields = ['goal_type', 'current_value', 'target_value', 'start_date', 'end_date', 'status', 'description', 'notes']
    success_url = reverse_lazy('goals:list')

    def get_queryset(self):
        return Goal.objects.filter(user=self.request.user)

class GoalDeleteView(LoginRequiredMixin, DeleteView):
    model = Goal
    template_name = 'goals/confirm_delete.html'
    success_url = reverse_lazy('goals:list')

    def get_queryset(self):
        return Goal.objects.filter(user=self.request.user)

def list(request):
    return HttpResponse('Заглушка для списка целей')

def add(request):
    return HttpResponse('Заглушка для добавления цели')

def detail(request, pk):
    return HttpResponse(f'Заглушка для просмотра цели {pk}')

def edit(request, pk):
    return HttpResponse(f'Заглушка для редактирования цели {pk}')

def delete(request, pk):
    return HttpResponse(f'Заглушка для удаления цели {pk}') 