from django import forms
from .models import Workout, WorkoutType

class WorkoutTypeForm(forms.ModelForm):
    class Meta:
        model = WorkoutType
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class WorkoutForm(forms.ModelForm):
    class Meta:
        model = Workout
        fields = ['workout_type', 'date', 'duration', 'intensity', 'calories_burned', 'notes']
        widgets = {
            'workout_type': forms.Select(attrs={'class': 'form-control'}),
            'date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'duration': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'intensity': forms.Select(attrs={'class': 'form-control'}),
            'calories_burned': forms.NumberInput(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        } 