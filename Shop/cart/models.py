from django.contrib.auth import get_user_model
from django.db import models
from django.utils.safestring import mark_safe

from products.models import ProductVariant

User = get_user_model()


# class OrderItem(models.Model):
#     cart = models.ForeignKey('Cart', on_delete=models.CASCADE)
#     product = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField(default=1)
#
#
# class Order(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)


class CartItem(models.Model):
    cart = models.ForeignKey('Cart', on_delete=models.CASCADE)
    product = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def get_price(self):
        # return self.product.get_current_price().format(self.quantity * self.product.price)
        return self.quantity * self.product.price

    def get_tage_price(self):
        return mark_safe(f'<p class="current_product_price">{self.get_price()}<span>₽</span></p>')

    def __str__(self):
        return f'Item id: {self.pk}, Product: {self.product.product.title}, quantity: {self.quantity} '


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def add_to_cart(self, product):
        item, created = CartItem.objects.get_or_create(cart=self, product=product)
        if not created:
            item.quantity += 1
            item.save()

    def decrease_item(self, product):
        item = CartItem.objects.get(cart=self, product=product)
        if item.quantity > 1:
            item.quantity -= 1
            item.save()
        else:
            item.delete()

    def remove_from_cart(self, product):
        item = CartItem.objects.get(cart=self, product=product)
        item.delete()

    def clear_cart(self):
        for item in CartItem.objects.filter(cart=self):
            item.delete()

    def get_cart_items(self):
        return CartItem.objects.filter(cart=self)

    def get_total(self):
        cart_items = self.get_cart_items()
        return sum(item.get_price() for item in cart_items)
