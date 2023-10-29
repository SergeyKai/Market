from django.db import models


class Expense(models.Model):
    description = models.CharField(max_length=200)  # Описание расходов
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Сумма расходов
    date = models.DateField()  # Дата расходов


class Sale(models.Model):
    # product = models.ForeignKey(Product, on_delete=models.CASCADE)  # Связь с товаром
    # customer = models.ForeignKey(Customer, on_delete=models.CASCADE)  # Связь с клиентом
    quantity = models.PositiveIntegerField()  # Количество проданных товаров
    sale_date = models.DateTimeField()  # Дата и время продажи


class Statistics(models.Model):
    date = models.DateField()  # Дата для статистики
    revenue = models.DecimalField(max_digits=10, decimal_places=2)  # Выручка на указанную дату
