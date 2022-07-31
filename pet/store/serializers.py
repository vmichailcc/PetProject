from rest_framework import serializers
from store.models import ProductCard, ProductComment


class ProductCardSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductCard
        fields = [
            "id",
            "name",
            "category",
            "vendor_code",
            "price",
            "old_price",
            "availability",
            "is_published",
            "created_at",
            "moderated_at",
            "description",
            "brand",
            "main_picture",
            "options",
            "attributes",
            "like",
        ]
        read_only_fields = ["like", "created_at", "moderated_at"]


class ProductCommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductComment
        fields = [
            "text_product",
            "text_author",
            "text",
            "text_created_at",
        ]
        read_only_fields = ["text_author", "text_created_at"]
