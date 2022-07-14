from django.db import models


class ProductCard(models.Model):
    id = models.CharField(verbose_name="ID", primary_key=True, max_length=100)
    name = models.CharField(verbose_name="Назва", max_length=200)
    category = models.ForeignKey("Category", on_delete=models.CASCADE, null=True, verbose_name="Категорія")
    vendor_code = models.CharField(verbose_name="Код товара", max_length=200)
    price = models.PositiveIntegerField(verbose_name="Ціна")
    old_price = models.IntegerField(default=0, verbose_name="Стара ціна")
    availability = models.BooleanField("Наявність", default=1)
    is_published = models.BooleanField("Публікація", default=1)
    created_at = models.DateTimeField(verbose_name="Час та дата створення", auto_now_add=True, null=True)
    moderated_at = models.DateTimeField(verbose_name="Дата оновленя", auto_now=True, null=True)
    description = models.TextField(verbose_name="Опис", max_length=5000)
    brand = models.CharField(verbose_name="Бренд", max_length=150)
    main_picture = models.ImageField(verbose_name="Головне зображення", blank=True, upload_to="uploadphoto/%d%m%Y/")
    options = models.JSONField(verbose_name="Опції", blank=True, null=True)
    attributes = models.JSONField(verbose_name="Атрибути", blank=True, null=True)
    card_views = models.IntegerField(verbose_name="Кількість переглядів", default=0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товари"


class Category(models.Model):
    category_id = models.CharField(primary_key=True, max_length=100)
    category_name = models.CharField(max_length=200)

    def __str__(self):
        return self.category_name

    class Meta:
        verbose_name = "Категорія"
        verbose_name_plural = "Категорії"

class Pictures(models.Model):
    pictures_point = models.ForeignKey(ProductCard, on_delete=models.CASCADE)
    pictures = models.ImageField(blank=True, upload_to="uploadphoto/%d%m%Y/")

    def __str__(self):
        return self.pictures_point, self.pk

    class Meta:
        verbose_name = "Зображення"
        verbose_name_plural = "Зображення"