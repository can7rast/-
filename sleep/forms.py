from django import forms
from .models import Sleep

class SleepForm(forms.ModelForm):
    class Meta:
        model = Sleep
        fields = ['date', 'start_time', 'end_time', 'quality', 'interruptions', 'notes']
        widgets = {
            'date': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control',
                    'placeholder': 'Выберите дату'
                }
            ),
            'start_time': forms.TimeInput(
                attrs={
                    'type': 'time',
                    'class': 'form-control',
                    'placeholder': 'Время отхода ко сну'
                }
            ),
            'end_time': forms.TimeInput(
                attrs={
                    'type': 'time',
                    'class': 'form-control',
                    'placeholder': 'Время пробуждения'
                }
            ),
            'quality': forms.Select(
                attrs={'class': 'form-control'}
            ),
            'interruptions': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'min': '0',
                    'placeholder': 'Количество пробуждений'
                }
            ),
            'notes': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': '3',
                    'placeholder': 'Заметки о сне'
                }
            )
        } 