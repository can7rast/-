from django import forms
from .models import Progress, PersonalRecord

class ProgressForm(forms.ModelForm):
    class Meta:
        model = Progress
        fields = ['date', 'weight', 'chest', 'waist', 'hips', 'biceps', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'weight': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'chest': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'waist': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'hips': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'biceps': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class PersonalRecordForm(forms.ModelForm):
    class Meta:
        model = PersonalRecord
        fields = ['date', 'exercise', 'weight', 'reps', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'exercise': forms.TextInput(attrs={'class': 'form-control'}),
            'weight': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'reps': forms.NumberInput(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        } 