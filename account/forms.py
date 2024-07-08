from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from .models import User

class UserLoginForm(AuthenticationForm):
    ROLE_CHOICES = [
        ('teacher', 'Teacher'),
        ('student', 'Student'),
    ]

    role = forms.ChoiceField(choices=ROLE_CHOICES, required=True)


class UserRegisterForm(UserCreationForm):
    is_teacher = forms.BooleanField(label='Register as a teacher', required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'is_teacher']