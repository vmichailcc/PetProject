from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import ProductCard, Pictures, ProductComment, Order


class ProductCardAdmin(admin.ModelAdmin):
    list_display = ("get_image", "name", "vendor_code", "brand",  "price", "old_price", "availability",
                    "is_published", "card_views")
    list_filter = ("brand", "price", "availability", "is_published", "card_views")
    list_editable = ("is_published", "availability")
    search_fields = ["name", "description", "brand", "id"]

    def get_image(self, obj):
        if obj.main_picture:
            return mark_safe(f"<img src='{obj.main_picture}' width='75'>")
        else:
            return "Без фото"
    get_image.short_description = "Фото"


class OrderAdmin(admin.ModelAdmin):
    list_display = ("order_number", "status", "created_at", "owner", )
    list_filter = ("status", )
    search_fields = ["order_number"]

    fields = ("order_number", ("product", "quantity"), "owner_comment", "status", "admin_comment", "owner")
    readonly_fields = ("owner", "order_number")


class ProductCommentAdmin(admin.ModelAdmin):
    list_display = ("text_product", "text_author", "text", "text_created_at", )


admin.site.register(ProductCard, ProductCardAdmin)
admin.site.register(Pictures)
admin.site.register(ProductComment, ProductCommentAdmin)
admin.site.register(Order)


admin.site.site_title = "STORE Адмін панель"
admin.site.site_header = "STORE Адмін панель"
