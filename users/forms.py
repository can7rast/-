from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, CoachAthlete

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'bio', 'role']

class CoachAthleteForm(forms.ModelForm):
    class Meta:
        model = CoachAthlete
        fields = ['athlete']
        widgets = {
            'athlete': forms.Select(attrs={'class': 'form-control'})
        }
    
    def __init__(self, coach, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['athlete'].queryset = User.objects.filter(
            is_coach=False
        ).exclude(
            id__in=CoachAthlete.objects.filter(coach=coach).values_list('athlete_id', flat=True)
        ) 