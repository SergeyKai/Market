from django.db import models
from django.contrib.auth import get_user_model

from products.models import ProductVariant

User = get_user_model()


class Expense(models.Model):
    description = models.CharField(max_length=200)  # Описание расходов
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Сумма расходов
    date = models.DateField()  # Дата расходов

    def __str__(self):
        return f'Expanse < amount: {self.amount}; date: {self.date}>'


class Sale(models.Model):
    product = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)  # Связь с клиентом
    quantity = models.PositiveIntegerField()  # Количество проданных товаров
    sale_date = models.DateTimeField(auto_now=True)  # Дата и время продажи

    def __str__(self):
        return f'Sale <product: {self.product.product.title}; customer: {self.customer.username}; quantity: {self.quantity}>'


class Revenue(models.Model):
    date = models.DateField(auto_now=True)  # Дата для статистики
    total_revenue = models.DecimalField(max_digits=10, decimal_places=2)  # Выручка на указанную дату

    def __str__(self):
        return f'Revenue <date: {self.date}; revenue: {self.total_revenue}>'
