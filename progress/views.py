from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Progress
from django.http import HttpResponse

class ProgressListView(LoginRequiredMixin, ListView):
    model = Progress
    template_name = 'progress/list.html'
    context_object_name = 'progress_list'

    def get_queryset(self):
        return Progress.objects.filter(user=self.request.user)

class ProgressDetailView(LoginRequiredMixin, DetailView):
    model = Progress
    template_name = 'progress/detail.html'
    context_object_name = 'progress'

class ProgressCreateView(LoginRequiredMixin, CreateView):
    model = Progress
    template_name = 'progress/form.html'
    fields = ['date', 'weight', 'chest', 'waist', 'hips', 'biceps', 'notes']
    success_url = reverse_lazy('progress:list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class ProgressUpdateView(LoginRequiredMixin, UpdateView):
    model = Progress
    template_name = 'progress/form.html'
    fields = ['date', 'weight', 'chest', 'waist', 'hips', 'biceps', 'notes']
    success_url = reverse_lazy('progress:list')

    def get_queryset(self):
        return Progress.objects.filter(user=self.request.user)

class ProgressDeleteView(LoginRequiredMixin, DeleteView):
    model = Progress
    template_name = 'progress/confirm_delete.html'
    success_url = reverse_lazy('progress:list')

    def get_queryset(self):
        return Progress.objects.filter(user=self.request.user)

def list(request):
    return HttpResponse('Заглушка для списка прогресса')

def add(request):
    return HttpResponse('Заглушка для добавления прогресса')

def detail(request, pk):
    return HttpResponse(f'Заглушка для просмотра прогресса {pk}')

def edit(request, pk):
    return HttpResponse(f'Заглушка для редактирования прогресса {pk}')

def delete(request, pk):
    return HttpResponse(f'Заглушка для удаления прогресса {pk}') 