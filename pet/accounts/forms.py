from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(label="Нік", help_text="Введить ім'я користувача для подальшої авторизації у системі", widget=forms.TextInput(attrs={'class': 'form-control'}),)
    first_name = forms.CharField(label="Ім'я", widget=forms.TextInput(attrs={'class': 'form-control'}), )
    last_name = forms.CharField(label="Прізвище", widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="Електрона пошта", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="Повторити пароль", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "password1", "password2")


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label="Нік", widget=forms.TextInput(attrs={'class': 'form-control'}), )
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class ContactForm(forms.Form):
    subject = forms.CharField(label="Тема", widget=forms.TextInput(attrs={'class': 'form-control'}))
    body = forms.CharField(label="Текст", widget=forms.Textarea(attrs={'class': 'form-control', "rows": 5}))

