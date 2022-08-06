from datetime import datetime, timedelta
from django.db.models import Sum, Count
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from django.views.generic.base import View
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from accounts.models import CustomUser
from .forms import AddProductComment
from .models import ProductCard, ProductComment, Pictures, Order
from .serializers import ProductCardSerializer, ProductCommentSerializer, OrderSerializer, ProductCardDetailSerializer, \
    OrderDetailSerializer


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


class StoreApiView(ListModelMixin, GenericViewSet):
    queryset = ProductCard.objects.all()
    serializer_class = ProductCardSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['brand', 'price']
    search_fields = ['name']

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.annotate(comments=Count('text_product'))
        return queryset

    @action(detail=True, methods=['post'])
    def add_like(self, request, pk=None):
        prod = self.get_object()
        prod.like += 1
        prod.save()
        serializer = self.get_serializer(prod)
        return Response(serializer.data)


class ProductDetailApiView(RetrieveModelMixin, GenericViewSet):
    serializer_class = ProductCardDetailSerializer
    queryset = ProductCard.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.annotate(comments_count=Count('text_product'))
        return queryset


class CommentApiView(CreateModelMixin, GenericViewSet):
    serializer_class = ProductCommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(**{'text_author': self.request.user})

    def get_queryset(self):
        user = self.request.user
        return ProductComment.objects.filter(text_author=user)


class OrderApiView(CreateModelMixin, ListModelMixin, GenericViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status']

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            user = self.request.user
            print("perform_create =", user)
            serializer.save(**{'owner': user})

    def get_queryset(self):
        user = self.request.user
        print(user.pk)
        return Order.objects.filter(owner=user.pk)


class OrderDetailApiView(RetrieveModelMixin, GenericViewSet):
    serializer_class = OrderDetailSerializer
    queryset = Order.objects.all()


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
        return render(request, "admin/dashboard.html", context)





