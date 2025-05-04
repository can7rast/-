from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Sleep
from django.http import HttpResponse

class SleepListView(LoginRequiredMixin, ListView):
    model = Sleep
    template_name = 'sleep/list.html'
    context_object_name = 'sleeps'

    def get_queryset(self):
        return Sleep.objects.filter(user=self.request.user)

class SleepDetailView(LoginRequiredMixin, DetailView):
    model = Sleep
    template_name = 'sleep/detail.html'
    context_object_name = 'sleep'

class SleepCreateView(LoginRequiredMixin, CreateView):
    model = Sleep
    template_name = 'sleep/form.html'
    fields = ['date', 'start_time', 'end_time', 'duration', 'quality', 'interruptions', 'notes']
    success_url = reverse_lazy('sleep:list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class SleepUpdateView(LoginRequiredMixin, UpdateView):
    model = Sleep
    template_name = 'sleep/form.html'
    fields = ['date', 'start_time', 'end_time', 'duration', 'quality', 'interruptions', 'notes']
    success_url = reverse_lazy('sleep:list')

    def get_queryset(self):
        return Sleep.objects.filter(user=self.request.user)

class SleepDeleteView(LoginRequiredMixin, DeleteView):
    model = Sleep
    template_name = 'sleep/confirm_delete.html'
    success_url = reverse_lazy('sleep:list')

    def get_queryset(self):
        return Sleep.objects.filter(user=self.request.user)

def list(request):
    return HttpResponse('Заглушка для списка сна')

def add(request):
    return HttpResponse('Заглушка для добавления сна')

def detail(request, pk):
    return HttpResponse(f'Заглушка для просмотра сна {pk}')

def edit(request, pk):
    return HttpResponse(f'Заглушка для редактирования сна {pk}')

def delete(request, pk):
    return HttpResponse(f'Заглушка для удаления сна {pk}') 