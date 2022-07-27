from django.shortcuts import render, get_object_or_404, get_list_or_404
from .models import ProductCard, ProductComment, Pictures
from django.views.generic.base import View
from .forms import AddProductComment


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
        comments = ProductComment.objects.filter(text_product=pk)
        form = AddProductComment
        context = {
            "product": product,
            "pictures": pictures,
            "comments": comments,
            "form": form,
        }
        return render(request, "store/product.html", context)

