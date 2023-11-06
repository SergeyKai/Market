from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('', views.cart_view, name='cart'),
    path('add_to_cart/<int:product_id>', views.add_to_cart, name='add_to_cart'),
    path('decrease_item/<int:product_id>', views.decrease_item, name='decrease_item'),
    path('remove_from_cart/<int:product_id>', views.remove_from_cart, name='remove_from_cart'),
    path('order', views.order, name='order'),
    path('success_order', views.success_order, name='success_order'),
]
