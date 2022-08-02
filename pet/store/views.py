from datetime import datetime, timedelta

from django.db.models import Sum, Count
from django.views.generic import ListView
from django.shortcuts import render, get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import ProductCard, ProductComment, Pictures, Order
from django.views.generic.base import View
from .forms import AddProductComment
from .serializers import ProductCardSerializer, ProductCommentSerializer, OrderSerializer
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated
from accounts.models import CustomUser


class ProductView(ListView):
    model = ProductCard
    template_name = "store/index.html"
    context_object_name = "products"
    paginate_by = 20


class ProductDetailView(View):

    def get(self, request, pk):
        product = get_object_or_404(ProductCard, pk=pk)
        pictures = Pictures.objects.filter(pictures_point=pk)
        comments = ProductComment.objects.filter(text_product=pk)
        form = AddProductComment
        context = {
            "product": product,
            "pictures": pictures,
            "comments": comments,
            "form": form,
        }
        return render(request, "store/product.html", context)




class StoreApiView(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    queryset = ProductCard.objects.all()
    serializer_class = ProductCardSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['brand', 'price']
    search_fields = ['name']

    @action(detail=True, methods=['post'])
    def add_like(self, request, pk=None):
        prod = self.get_object()
        prod.like += 1
        prod.save()
        serializer = self.get_serializer(prod)
        return Response(serializer.data)


class CommentApiView(ModelViewSet):
    serializer_class = ProductCommentSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post']

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(**{'text_author': self.request.user})

    def get_queryset(self):
        user = self.request.user
        return ProductComment.objects.filter(text_author=user)


class OrderApiView(ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post']

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(**{'owner': self.request.user})

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(owner=user)


class DashboardView(View):

    def get(self, request):
        user_count = CustomUser.objects.count()
        user_count_last_week = CustomUser.objects.filter(
            date_joined__range=[datetime.now() - timedelta(weeks=1), datetime.now()]
        ).count()
        orders_count = Order.objects.count()
        orders_count_last_week = Order.objects.filter(
            created_at__range=[datetime.now() - timedelta(weeks=1), datetime.now()]
        ).count()
        products_count = ProductCard.objects.count()
        likes = ProductCard.objects.aggregate(Sum('like'))
        comments = len(ProductComment.objects.annotate(Count('text')))

        context = {
            "user_count": user_count,
            "user_count_last_week": user_count_last_week,
            "orders_count": orders_count,
            "orders_count_last_week": orders_count_last_week,
            "products_count": products_count,
            "likes": likes['like__sum'],
            "comments": comments,
        }
        return render(request, "store/dashboard.html", context)
