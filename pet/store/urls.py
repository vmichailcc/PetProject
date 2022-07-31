
from django.urls import path
from .views import ProductView, ProductDetailView, StoreApiView, CommentApiView, OrderApiView
from rest_framework import routers

store_router = routers.SimpleRouter()
store_router.register('', StoreApiView, basename='store')

comment_router = routers.SimpleRouter()
comment_router.register('', CommentApiView, basename='comment')

order_router = routers.SimpleRouter()
order_router.register('', OrderApiView, basename='comment')

urlpatterns = [
    path('', ProductView.as_view(), name='index'),
    path("product/<str:pk>", ProductDetailView.as_view(), name="product")
]
