from django.urls import path
from . import views

urlpatterns = [
    path('update_profile/<int:pk>/', views.UpdateProfileView.as_view(), name='update_profile'),
    path('login/', views.LoginUserView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('register/', views.Register.as_view(), name='register'),
    path('invalid_verify/', views.InvalidVerifyView.as_view(), name='invalid_verify'),
    path('confirm_email/', views.ConfirmView.as_view(), name='confirm_email'),
    path('accounts/profile/', views.ProfileView.as_view(), name='profile'),
    path("verify_email/<uidb64>/<token>/", views.VerifyEmail.as_view(), name="verify_email"),
]
