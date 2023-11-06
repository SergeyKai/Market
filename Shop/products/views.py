from django.shortcuts import render
from django.views.generic import ListView, CreateView, DetailView

from .models import Product, ProductImage, ProductVariant


class ProductList(ListView):
    model = Product
    template_name = 'products/products.html'
    context_object_name = 'products'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        products = context['products']
        product_data = []

        for product in products:
            product_variant = ProductVariant.objects.filter(product=product.pk).first()
            product_image = ProductImage.objects.filter(product=product.pk).first()

            product_data.append({'product': product, 'image': product_image, 'product_variant': product_variant})

        context['product_data'] = product_data
        return context

    def get_queryset(self):
        category_pk = self.kwargs.get('category_pk')

        if category_pk is not None:
            products = self.model.objects.filter(category=category_pk)
            return products
        else:
            return super().get_queryset()


class ProductInstance(DetailView):
    template_name = 'products/product_instance.html'
    context_object_name = 'product'

    def get_object(self):
        product_pk = self.kwargs.get('product_pk')
        product = Product.objects.get(pk=product_pk)
        variant_pk = self.request.GET.get('variant', None)
        if variant_pk is not None:
            product_variants = ProductVariant.objects.filter(product=product)
            current_variant = product_variants.get(pk='variant_pk')
            images = ProductImage.objects.filter(product=current_variant)
            return {
                'product': product,
                'current_variant': current_variant,
                'product_variants': product_variants,
                'images': images
            }
        else:
            product_variants = ProductVariant.objects.filter(product=product)
            current_variant = product_variants.first()
            images = ProductImage.objects.filter(product=current_variant)
            return {
                'product': product,
                'current_variant': current_variant,
                'product_variants': product_variants,
                'images': images
            }

# {
#   "вес": "1.5 кг",
#   "размер": "Средний",
#   "материал": "Хлопок"
# }
