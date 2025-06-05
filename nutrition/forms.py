from django import forms
from .models import Meal
from tempus_dominus.widgets import DatePicker, TimePicker

class MealForm(forms.ModelForm):
    class Meta:
        model = Meal
        fields = ['meal_type', 'date', 'time', 'calories', 'protein', 'fat', 'carbs', 'notes']
        widgets = {
            'meal_type': forms.Select(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Выберите тип приема пищи'
                }
            ),
            'date': DatePicker(
                attrs={
                    'class': 'form-control datetimepicker-input',
                    'data-target': '#datepicker',
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
            'time': TimePicker(
                attrs={
                    'class': 'form-control datetimepicker-input',
                    'data-target': '#timepicker',
                    'placeholder': 'Выберите время'
                },
                options={
                    'format': 'HH:mm',
                    'locale': 'ru',
                    'stepping': 5,
                    'buttons': {
                        'showClear': True,
                        'showClose': True
                    }
                }
            ),
            'calories': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Введите количество калорий',
                    'min': '0'
                }
            ),
            'protein': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Введите количество белков (г)',
                    'min': '0',
                    'step': '0.1'
                }
            ),
            'fat': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Введите количество жиров (г)',
                    'min': '0',
                    'step': '0.1'
                }
            ),
            'carbs': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Введите количество углеводов (г)',
                    'min': '0',
                    'step': '0.1'
                }
            ),
            'notes': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': '3',
                    'placeholder': 'Заметки о приеме пищи'
                }
            )
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.pk:
            self.fields['date'].initial = forms.DateField().to_python(None)
            self.fields['time'].initial = forms.TimeField().to_python(None) 