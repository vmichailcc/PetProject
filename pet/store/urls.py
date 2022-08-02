
from django.urls import path
from .views import ProductView, ProductDetailView, StoreApiView, CommentApiView, OrderApiView, DashboardView
from rest_framework import routers

store_router = routers.SimpleRouter()
store_router.register('', StoreApiView, basename='store_router')

comment_router = routers.SimpleRouter()
comment_router.register('', CommentApiView, basename='comment_router')

order_router = routers.SimpleRouter()
order_router.register('', OrderApiView, basename='order_router')

urlpatterns = [
    path('', ProductView.as_view(), name='index'),
    path("product/<str:pk>", ProductDetailView.as_view(), name="product"),
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
]
