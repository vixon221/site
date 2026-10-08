from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название категории")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

class Dish(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='dishes', verbose_name="Категория")
    name = models.CharField(max_length=150, verbose_name="Название блюда")
    description = models.TextField(verbose_name="Описание", blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Цена (сом)")
    image_url = models.URLField(verbose_name="Ссылка на изображение", blank=True, default="https://via.placeholder.com/300")
    is_available = models.BooleanField(default=True, verbose_name="В наличии")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Блюдо"
        verbose_name_plural = "Блюда"

# --- НОВАЯ МОДЕЛЬ: Филиалы / Заведения (2GIS) ---
class Restaurant(models.Model):
    title = models.CharField(max_length=150, verbose_name="Название филиала/ресторана")
    address = models.CharField(max_length=255, verbose_name="Адрес")
    phone = models.CharField(max_length=50, verbose_name="Телефон", blank=True)
    gis_url = models.URLField(verbose_name="Ссылка на 2GIS", blank=True, help_text="Вставьте ссылку на филиал в 2GIS")

    def __str__(self):
        return f"{self.title} ({self.address})"

    class Meta:
        verbose_name = "Филиал/Заведение"
        verbose_name_plural = "Филиалы/Заведения"