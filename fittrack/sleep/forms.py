from django import forms
from .models import Sleep

class SleepForm(forms.ModelForm):
    class Meta:
        model = Sleep
        fields = ['date', 'start_time', 'end_time', 'quality', 'interruptions', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'quality': forms.Select(attrs={'class': 'form-control'}),
            'interruptions': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        } 