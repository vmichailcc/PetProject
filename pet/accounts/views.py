from django.contrib import messages
from django.contrib.auth import login, logout
from django.shortcuts import redirect, render
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import FormView, TemplateView
from .forms import UserRegisterForm, UserLoginForm


class Register(View):
    template_name = 'accounts/register.html'

    def get(self, request):
        context = {
            "form": UserRegisterForm()
        }
        return  render(request, self.template_name, context)

    def post(self, request):
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Вітаю! Ви зареєстровані!')
            return redirect("index")
        context = {
            "form": form
        }
        return  render(request, self.template_name, context)



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


class ConfirmView(TemplateView):
    template_name = 'accounts/confirm_email.html'
