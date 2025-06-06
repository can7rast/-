from django import forms
from .models import Workout
from tempus_dominus.widgets import DatePicker

class WorkoutForm(forms.ModelForm):
    duration = forms.IntegerField(
        min_value=1,
        max_value=1440,  # 24 часа в минутах
        required=True,
        label='Продолжительность (мин)',
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите продолжительность в минутах'
        })
    )

    class Meta:
        model = Workout
        fields = ['workout_type', 'date', 'intensity', 'notes']
        widgets = {
            'workout_type': forms.Select(
                attrs={'class': 'form-control'}
            ),
            'date': DatePicker(
                attrs={
                    'class': 'form-control datetimepicker-input',
                    'data-target': '#datetimepicker1',
                    'placeholder': 'Выберите дату'
                },
                options={
                    'useCurrent': True,
                    'locale': 'ru',
                    'format': 'L',
                    'buttons': {
                        'showToday': True,
                        'showClear': True,
                        'showClose': True
                    },
                    'icons': {
                        'time': 'far fa-clock',
                        'date': 'far fa-calendar',
                        'up': 'fas fa-arrow-up',
                        'down': 'fas fa-arrow-down',
                        'previous': 'fas fa-chevron-left',
                        'next': 'fas fa-chevron-right',
                        'today': 'fas fa-calendar-check',
                        'clear': 'fas fa-trash',
                        'close': 'fas fa-times'
                    }
                }
            ),
            'intensity': forms.Select(
                attrs={'class': 'form-control'}
            ),
            'notes': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': '3',
                    'placeholder': 'Заметки о тренировке'
                }
            )
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.pk:
            self.fields['date'].initial = forms.DateField().to_python(None)
        elif hasattr(self.instance, 'duration'):
            self.fields['duration'].initial = self.instance.duration

    def clean_duration(self):
        duration = self.cleaned_data['duration']
        if duration <= 0:
            raise forms.ValidationError('Продолжительность тренировки должна быть больше 0 минут')
        if duration > 1440:
            raise forms.ValidationError('Продолжительность тренировки не может превышать 24 часа (1440 минут)')
        return duration

    def save(self, commit=True):
        workout = super().save(commit=False)
        workout.duration = self.cleaned_data['duration']
        # Рассчитываем сожженные калории
        base_calories = {
            'cardio': 8,  # калорий в минуту при средней интенсивности
            'strength': 6,
            'hiit': 10,
            'yoga': 4,
            'stretching': 3,
            'other': 5
        }
        
        intensity_multiplier = {
            'low': 0.8,
            'medium': 1.0,
            'high': 1.2
        }
        
        workout.calories_burned = int(
            workout.duration * 
            base_calories[workout.workout_type] * 
            intensity_multiplier[workout.intensity]
        )
        
        if commit:
            workout.save()
        return workout 