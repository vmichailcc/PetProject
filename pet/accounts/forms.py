from django.utils.translation import gettext as _
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from .utils import send_verify_email
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

    error_messages = {
        "invalid_login": _(
            "Please enter a correct %(username)s and password. Note that both "
            "fields may be case-sensitive."
        ),
        "inactive": _("This account is inactive."),
    }

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        email = self.cleaned_data.get('username')
        print("username =", username)
        print("password =", password)
        print("email =", email)
        if username is not None and password:
            self.user_cache = authenticate(
                self.request,
                username=username,
                password=password,
            )
            print("user_cache = ", self.user_cache)
            if not self.user_cache.email_verify:
                send_verify_email(self.request, self.user_cache)
                raise ValidationError(
                    "Електронна пошта не веріфікована. Будь ласка, перевірте пошту!",
                    code='invalid_login'
                )

            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data


class UpdateUserForm(forms.ModelForm):
    first_name = forms.CharField(label="Ім'я", widget=forms.TextInput(attrs={'class': 'form-control'}), )
    last_name = forms.CharField(label="Прізвище", widget=forms.TextInput(attrs={'class': 'form-control'}))
    city = forms.CharField(label="Місто", widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = CustomUser
        fields = ("first_name", "last_name", "city")

