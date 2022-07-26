from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser


class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField(label="Ім'я", widget=forms.TextInput(attrs={'class': 'form-control'}), )
    last_name = forms.CharField(label="Прізвище", widget=forms.TextInput(attrs={'class': 'form-control'}))
    city = forms.CharField(label="Місто", widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="Електрона пошта", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="Повторити пароль", widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = CustomUser
        fields = ("email", "first_name", "last_name", "city", "password1", "password2")


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label="Електрона пошта", widget=forms.TextInput(attrs={'class': 'form-control'}), )
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
