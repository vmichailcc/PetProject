from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import ProductCard, Category, Pictures


class ProductCardAdmin(admin.ModelAdmin):
    list_display = ("get_image", "name", "vendor_code", "brand", "category", "price", "old_price", "availability",
                    "is_published", "card_views", "created_at", "moderated_at")
    list_filter = ("brand", "category", "price", "availability", "is_published", "card_views")
    list_editable = ("is_published",)
    search_fields = ["name", "description", "brand", "id"]

    def get_image(self, obj):
        if obj.main_picture:
            return mark_safe(f"<img src='{obj.main_picture}' width='75'>")
        else:
            return "Без фото"
    get_image.short_description = "Фото"


admin.site.register(ProductCard, ProductCardAdmin)
admin.site.register(Category)
admin.site.register(Pictures)

admin.site.site_title = "STORE Адмін панель"
admin.site.site_header = "STORE Адмін панель"
