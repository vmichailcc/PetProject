from django.views.generic import ListView, DetailView
from django.shortcuts import render, get_object_or_404
from .models import ProductCard, ProductComment, Pictures
from django.views.generic.base import View
from .forms import AddProductComment
from .serializers import ProductCardSerializer, ProductCommentSerializer
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin
from rest_framework.permissions import IsAuthenticated, IsAdminUser
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


class StoreApiView(ListModelMixin, GenericViewSet):
    queryset = ProductCard.objects.all()
    serializer_class = ProductCardSerializer


class CommentApiView(ListModelMixin, CreateModelMixin, GenericViewSet):
    queryset = ProductComment.objects.all()
    serializer_class = ProductCommentSerializer

    def perform_create(self, serializer):
        print(self.request.user)
        if self.request.user.is_authenticated:
            serializer.save(**{'text_author': self.request.user})






