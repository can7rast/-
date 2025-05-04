from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Prediction
from django.http import HttpResponse

class PredictionListView(LoginRequiredMixin, ListView):
    model = Prediction
    template_name = 'predictions/list.html'
    context_object_name = 'predictions'

    def get_queryset(self):
        return Prediction.objects.filter(user=self.request.user)

class PredictionDetailView(LoginRequiredMixin, DetailView):
    model = Prediction
    template_name = 'predictions/detail.html'
    context_object_name = 'prediction'

class PredictionCreateView(LoginRequiredMixin, CreateView):
    model = Prediction
    template_name = 'predictions/form.html'
    fields = ['prediction_type', 'current_value', 'predicted_value', 'prediction_date', 'target_date', 'confidence', 'notes']
    success_url = reverse_lazy('predictions:list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class PredictionUpdateView(LoginRequiredMixin, UpdateView):
    model = Prediction
    template_name = 'predictions/form.html'
    fields = ['prediction_type', 'current_value', 'predicted_value', 'prediction_date', 'target_date', 'confidence', 'notes']
    success_url = reverse_lazy('predictions:list')

    def get_queryset(self):
        return Prediction.objects.filter(user=self.request.user)

class PredictionDeleteView(LoginRequiredMixin, DeleteView):
    model = Prediction
    template_name = 'predictions/confirm_delete.html'
    success_url = reverse_lazy('predictions:list')

    def get_queryset(self):
        return Prediction.objects.filter(user=self.request.user)

def list(request):
    return HttpResponse('Заглушка для списка прогнозов')

def add(request):
    return HttpResponse('Заглушка для добавления прогноза')

def detail(request, pk):
    return HttpResponse(f'Заглушка для просмотра прогноза {pk}')

def edit(request, pk):
    return HttpResponse(f'Заглушка для редактирования прогноза {pk}')

def delete(request, pk):
    return HttpResponse(f'Заглушка для удаления прогноза {pk}') 