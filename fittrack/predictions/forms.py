from django import forms
from .models import Prediction

class PredictionForm(forms.ModelForm):
    class Meta:
        model = Prediction
        fields = ['prediction_type', 'current_value', 'predicted_value', 'prediction_date', 'target_date', 'confidence', 'notes']
        widgets = {
            'prediction_type': forms.Select(attrs={'class': 'form-control'}),
            'current_value': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'predicted_value': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'prediction_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'target_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'confidence': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'min': '0', 'max': '100'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        } 