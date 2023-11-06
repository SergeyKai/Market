from django.contrib import admin
from django.urls import path, include

from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.ProductList.as_view(), name='products_list'),
    path('<int:category_pk>', views.ProductList.as_view(), name='products_list_category_filter'),
    path('instance/<int:product_pk>/', views.ProductInstance.as_view(), name='product_instance'),
    path('instance/<int:product_pk>/<int:variant_pk>', views.ProductInstance.as_view(), name='product_instance_variant'),
]
