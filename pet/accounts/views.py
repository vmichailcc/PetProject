from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy, reverse
from django.views.generic import FormView, TemplateView, UpdateView
from .forms import UserRegisterForm, UserLoginForm, UpdateUserForm
from .utils import send_verify_email
from django.core.exceptions import ValidationError
from django.utils.http import urlsafe_base64_decode
from django.views import View
from django.contrib.auth.tokens import default_token_generator as token_generator
from .models import CustomUser


class Register(View):
    template_name = 'accounts/register.html'

    def get(self, request):
        context = {
            "form": UserRegisterForm()
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=password)
            print(request)
            print(user)
            send_verify_email(request, user)
            return redirect("confirm_email")
        context = {
            "form": form
        }
        return render(request, self.template_name, context)


class LoginFormView(LoginView):
    form_class = UserLoginForm
    success_url = reverse_lazy('index')
    template_name = 'accounts/login.html'

    def form_valid(self, form):
        self.user = form.get_user()
        login(self.request, self.user)
        return super().form_valid(form)


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect(reverse('index'))


class ConfirmView(TemplateView):
    template_name = 'accounts/confirm_email.html'


class InvalidVerifyView(TemplateView):
    template_name = 'accounts/invalid_verify.html'


class VerifyEmail(View):
    def get(self, request, uidb64, token):
        user = self.get_user(uidb64)
        if user is not None and token_generator.check_token(user, token):
            user.email_verify = True
            user.save()
            login(request, user)
            return redirect('index')
        return redirect('invalid_verify')

    @staticmethod
    def get_user(uidb64):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = CustomUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError,
                CustomUser.DoesNotExist, ValidationError):
            user = None
        return user


class UpdateUserView(UpdateView):
    model = CustomUser

    fields = ['first_name', 'last_name', 'city']
    template_name = 'accounts/profile.html'

    # def get_queryset(self):
    #     return CustomUser.objects.filter(id=self.request.user.id)
