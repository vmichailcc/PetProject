from django.urls import path
from .views import LoginFormView, LogoutView, RegistrerFormUser


urlpatterns = [
    path('login/', LoginFormView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegistrerFormUser.as_view(), name='register')
]

