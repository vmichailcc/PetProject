from django.contrib import admin
from .models import CustomUser
from store.models import Order
'''
Список всіх користувачів які зареєструвались на сайті:
-	Ім'я;
-	Прізвище;
-	Місто;
-	Кількість замовлень. Пошук по імені і прізвищу.
'''


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("email", "first_name", "last_name", "city", "order_count")
    search_fields = ["first_name", "last_name"]

    def order_count(self, obj):
        count = Order.objects.filter(owner=obj)
        return len(count)

    order_count.short_description = "Кількість замовлень"


admin.site.register(CustomUser, CustomUserAdmin)
