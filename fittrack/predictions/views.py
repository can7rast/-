from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Prediction
from .forms import PredictionForm

@login_required
def prediction_list(request):
    predictions = Prediction.objects.filter(user=request.user).order_by('-prediction_date')
    return render(request, 'predictions/list.html', {'predictions': predictions})

@login_required
def prediction_detail(request, pk):
    prediction = get_object_or_404(Prediction, pk=pk, user=request.user)
    return render(request, 'predictions/detail.html', {'prediction': prediction})

@login_required
def prediction_create(request):
    if request.method == 'POST':
        form = PredictionForm(request.POST)
        if form.is_valid():
            prediction = form.save(commit=False)
            prediction.user = request.user
            prediction.save()
            messages.success(request, 'Предсказание успешно добавлено')
            return redirect('predictions:list')
    else:
        form = PredictionForm()
    return render(request, 'predictions/form.html', {'form': form, 'title': 'Добавить предсказание'})

@login_required
def prediction_delete(request, pk):
    prediction = get_object_or_404(Prediction, pk=pk, user=request.user)
    if request.method == 'POST':
        prediction.delete()
        messages.success(request, 'Предсказание успешно удалено')
        return redirect('predictions:list')
    return render(request, 'predictions/confirm_delete.html', {'prediction': prediction}) 