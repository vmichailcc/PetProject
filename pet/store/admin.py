from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import ProductCard, Category, Pictures


class ProductCardAdmin(admin.ModelAdmin):
    list_display = ("get_image", "name", "vendor_code", "brand", "category", "price", "old_price", "availability",
                    "is_published", "card_views")

    def get_image(self, obj):
        if obj.main_picture:
            return mark_safe(f"<img src='{obj.main_picture}' width='75'>")
        else:
            return "Без фото"

    get_image.short_description = "Фото"


    """
    From SPro admin:
    search_fields = ["title", "description", "author_id"]
    list_filter = ["title", "author_id"]
    list_editable = ["title", "description"]
    radio_fields = {"author_id": admin.HORIZONTAL}
    """
admin.site.register(ProductCard, ProductCardAdmin)
admin.site.register(Category)
admin.site.register(Pictures)

admin.site.site_title = "STORE Адмін панель"
admin.site.site_header = "STORE Адмін панель"
