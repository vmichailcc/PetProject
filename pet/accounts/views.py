from django.contrib.auth import login, logout
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import FormView
from .forms import UserRegisterForm, UserLoginForm


class RegistrerFormUser(FormView):
    form_class = UserRegisterForm
    success_url = reverse_lazy('index')
    template_name = 'accounts/register.html'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class LoginFormView(FormView):
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
