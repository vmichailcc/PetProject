from django.shortcuts import render, get_object_or_404, get_list_or_404
from .models import ProductCard, Category, Pictures
from django.views.generic.base import View


class ProductView(View):
    def get(self, request):
        products = ProductCard.objects.all()
        context = {
            "products": products,
        }
        return render(request, "store/index.html", context)


class ProductDetailView(View):
    def get(self, request, pk):
        product = get_object_or_404(ProductCard, pk=pk)
        pictures = Pictures.objects.filter(pictures_point=pk)
        context = {
            "product": product,
            "pictures": pictures,
        }
        return render(request, "store/product.html", context)
