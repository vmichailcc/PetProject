from django.urls import path
from .views import LoginUserView, LogoutView, Register, ConfirmView, VerifyEmail, InvalidVerifyView, UpdateUserView

urlpatterns = [
    path('login/', LoginUserView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', Register.as_view(), name='register'),
    path('invalid_verify/', InvalidVerifyView.as_view(), name='invalid_verify'),
    path('confirm_email/', ConfirmView.as_view(), name='confirm_email'),
    path('accounts/profile/', UpdateUserView.as_view(), name='profile'),
    path("verify_email/<uidb64>/<token>/", VerifyEmail.as_view(), name="verify_email"),
]
