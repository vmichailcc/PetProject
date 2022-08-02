from django.db.models import Count
from rest_framework import serializers
from store.models import ProductCard, ProductComment, Order


class ProductCardSerializer(serializers.ModelSerializer):
    comments = serializers.IntegerField()

    class Meta:
        model = ProductCard
        fields = [
            "name",
            "brand",
            "main_picture",
            "like",
            'comments',
        ]
        read_only_fields = [
            "name",
            "brand",
            "main_picture",
        ]

    def get_comments(self, obj):
        return len(obj.comments)


class ProductCardDetailSerializer(serializers.ModelSerializer):
    comments = serializers.CharField()
    comments_count = serializers.IntegerField(default=0)
    pictures = serializers.ImageField(default=0)

    class Meta:
        model = ProductCard
        fields = [
            "name",
            "description",
            "brand",
            "main_picture",
            "pictures",
            "comments_count",
            "comments",
            "like",
        ]
        read_only_fields = ["like"]

    def get_comments(self, obj):
        return len(obj.comments)

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


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = [
            "product",
            "quantity",
            "owner_comment",
            "status",
            ]
        read_only_fields = ["status"]


class OrderDetailSerializer(serializers.ModelSerializer):
    product = serializers.CharField()
    class Meta:
        model = Order
        fields = [
            "product",
            "quantity",
            "status",
            "owner_comment",
            "admin_comment"
        ]
        read_only_fields = [
            "product",
            "quantity",
            "status",
            "owner_comment",
            "admin_comment"
        ]