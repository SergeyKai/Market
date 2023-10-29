from django.db import models
from django.utils.safestring import mark_safe


class Supplier(models.Model):
    """
    class: Supplier
    Модель поставщика товаров
    """
    title = models.CharField(max_length=200)
    address = models.CharField(max_length=200)

    def __str__(self):
        return f'Supplier: {self.title}; id: {self.pk}'


class Category(models.Model):
    """
    class: Category
    """
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=100, null=True)

    def __str__(self):
        return f'Category: {self.title}; id: {self.pk}'


class Product(models.Model):
    """
    class: Product
    Модель товаров
    """
    title = models.CharField(max_length=200)
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True)
    prise = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now=True)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f'Product: {self.title}; id: {self.pk}'


class Color(models.Model):
    """
    class: Color
    Модель вариации цветов продукта
    """
    title = models.CharField(max_length=100)
    code = models.CharField(max_length=10)

    def __str__(self):
        return f'Color: {self.title}; id: {self.pk}'

    def get_color(self):
        return mark_safe(f'<span class="furniture_color_example" style="background:{self.code}"></span>')


class ProductVariant(models.Model):
    """
    class: ProductVariant
    Данная модель необхадима для различных вариаций одного продукта
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    availability = models.BooleanField(default=True)
    attributes = models.JSONField()

    def __str__(self):
        return f'Product: {self.product.title}; Color: {self.color.title}; id: {self.pk}'


class ProductImage(models.Model):
    """
    class: ProductImage
    Модель изображений продукта
    """
    product = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products')

    def __str__(self):
        return f'Image id:{self.pk}; Product: {self.product.product.title}'
