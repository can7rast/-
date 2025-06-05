from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Profile, CoachAthlete
from django.contrib.auth import authenticate

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'birth_date', 'gender', 'height', 'weight', 'bio']
        widgets = {
            'birth_date': forms.DateInput(attrs={
                'class': 'form-control datetimepicker-input',
                'data-target': '#birth_date',
                'data-toggle': 'datetimepicker'
            }),
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4
            })
        }

class CoachAthleteForm(forms.ModelForm):
    class Meta:
        model = CoachAthlete
        fields = ['athlete']

    def __init__(self, coach=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if coach:
            # Исключаем текущего тренера и уже связанных спортсменов
            existing_athletes = CoachAthlete.objects.filter(coach=coach).values_list('athlete', flat=True)
            self.fields['athlete'].queryset = User.objects.exclude(
                id__in=list(existing_athletes) + [coach.id]
            )

class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        
        if username and password:
            user = authenticate(username=username, password=password)
            if user is None:
                raise forms.ValidationError('Нет пользователя с такими данными')
        return cleaned_data 