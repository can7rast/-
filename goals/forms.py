from django import forms
from .models import Goal

class GoalForm(forms.ModelForm):
    class Meta:
        model = Goal
        fields = ['title', 'description', 'goal_type', 'target_value', 
                 'current_value', 'start_date', 'target_date', 'status']
        widgets = {
            'start_date': forms.DateInput(attrs={'class': 'datetimepicker-input', 
                                               'data-target': '#start_date'}),
            'target_date': forms.DateInput(attrs={'class': 'datetimepicker-input', 
                                                'data-target': '#target_date'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        } 