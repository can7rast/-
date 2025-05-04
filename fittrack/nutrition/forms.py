from django import forms
from .models import Meal

class MealForm(forms.ModelForm):
    class Meta:
        model = Meal
        fields = ['date', 'meal_type', 'time', 'calories', 'protein', 'fat', 'carbs', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'meal_type': forms.Select(attrs={'class': 'form-control'}),
            'time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'calories': forms.NumberInput(attrs={'class': 'form-control'}),
            'protein': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'fat': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'carbs': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        } 