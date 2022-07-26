from django.urls import path
from .views import LoginFormView, LogoutView, Register, ConfirmView

urlpatterns = [
    path('login/', LoginFormView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', Register.as_view(), name='register'),
    path('confirm_email/', ConfirmView.as_view(), name='confirm_email'),
]

