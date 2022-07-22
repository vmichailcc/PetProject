from django.db import models
from django.urls import reverse
from django.utils.safestring import mark_safe


class ProductCard(models.Model):
    id = models.CharField(verbose_name="ID", primary_key=True, max_length=100)
    name = models.CharField(verbose_name="Назва", max_length=200)
    category = models.ForeignKey("Category", on_delete=models.CASCADE, null=True, verbose_name="Категорія")
    vendor_code = models.CharField(verbose_name="Код товара", max_length=200)
    price = models.PositiveIntegerField(verbose_name="Ціна")
    old_price = models.IntegerField(default=0, verbose_name="Стара ціна")
    availability = models.BooleanField("Наявність", default=1)
    is_published = models.BooleanField("Публікація", default=1)
    created_at = models.DateTimeField(verbose_name="Час створення", auto_now_add=True)
    moderated_at = models.DateTimeField(verbose_name="Час оновленя", auto_now=True)
    description = models.TextField(verbose_name="Опис", max_length=5000)
    brand = models.CharField(verbose_name="Бренд", max_length=150)
    main_picture = models.ImageField(verbose_name="Головне зображення", blank=True, upload_to="uploadphoto/%d%m%Y/")
    options = models.JSONField(verbose_name="Опції", blank=True, null=True)
    attributes = models.JSONField(verbose_name="Атрибути", blank=True, null=True)
    card_views = models.IntegerField(verbose_name="Перегляди", default=0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товари"

    def get_absolute_url(self):
        return reverse("view_card", kwargs={"pk": self.pk})


class Category(models.Model):
    category_id = models.CharField(verbose_name="ID категорії", primary_key=True, max_length=100)
    category_name = models.CharField(verbose_name="Назва категорії", max_length=200)

    def __str__(self):
        return self.category_name

    def get_absolute_url(self):
        return reverse("category", kwargs={"pk": self.pk})

    class Meta:
        verbose_name = "Категорія"
        verbose_name_plural = "Категорії"


class Pictures(models.Model):
    pictures_point = models.ForeignKey(
        ProductCard, on_delete=models.CASCADE,
        verbose_name="Назва товару що зображен",
        related_name="image",
    )
    pictures = models.ImageField(blank=True, upload_to="uploadphoto/%d%m%Y/", verbose_name="Назва зображення")

    # def __str__(self):
    #     return self.pictures_point

    def get_absolute_url(self):
        return reverse("pictures", kwargs={"pk": self.pk})

    class Meta:
        verbose_name = "Зображення"
        verbose_name_plural = "Зображення"
