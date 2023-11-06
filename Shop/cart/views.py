from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required

from statistic.models import Revenue, Sale
from products.models import ProductVariant
from .models import Cart


@login_required
def cart_view(request):
    cart = Cart.objects.get(user=request.user)
    return render(request, 'cart/cart.html', {'cart': cart, 'cart_items': cart.get_cart_items()})


@login_required
def add_to_cart(request, product_id):
    cart = Cart.objects.get(user=request.user)
    product = ProductVariant.objects.get(pk=product_id)
    cart.add_to_cart(product)
    return redirect('cart')


@login_required
def decrease_item(request, product_id):
    cart = Cart.objects.get(user=request.user)
    product = ProductVariant.objects.get(pk=product_id)
    cart.decrease_item(product)
    return redirect('cart')


@login_required
def remove_from_cart(request, product_id):
    cart = Cart.objects.get(user=request.user)
    product = ProductVariant.objects.get(pk=product_id)
    cart.remove_from_cart(product)
    return redirect('cart')


@login_required
def order(request):
    cart = Cart.objects.get(user=request.user)
    if request.method == 'POST':
        for item in cart.get_cart_items():
            sale = Sale.objects.create(
                product=item.product,
                customer=request.user,
                quantity=item.quantity,
            )
            try:
                revenue = Revenue.objects.get(date=timezone.now())
                revenue.total_revenue += item.get_price()
                revenue.save()
            except Revenue.DoesNotExist:
                Revenue.objects.create(
                    date=timezone.now(),
                    total_revenue=item.get_price()
                )
            product = item.product
            if product.quantity > item.quantity:
                product.quantity -= item.quantity
            else:
                product.quantity = 0
                product.availability = False

            product.save()

        cart.clear_cart()
        return redirect('success_order')

    return redirect('cart')
    # return render(request, 'cart/order.html', {'cart': cart})


@login_required
def success_order(request):
    return render(request, 'cart/success_order.html')
