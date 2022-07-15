from django.urls import path
from .views import ProductView, ProductDetailView


urlpatterns = [
    path('', ProductView.as_view(), name='index'),
    path("product/<str:pk>", ProductDetailView.as_view(), name="product")
]
