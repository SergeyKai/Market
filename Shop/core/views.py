from django.shortcuts import render

from products.models import Category, Product, ProductVariant, ProductImage


def index(request):
    categories = Category.objects.all()
    products_query = Product.objects.all()[:3]
    products_list = []
    for product in products_query:
        product_variant = ProductVariant.objects.filter(product=product).first()
        product_image = ProductImage.objects.filter(product=product_variant).first
        products_list.append(
            {
                'product': product,
                'product_variant': product_variant,
                'image': product_image,
            }
        )
    return render(request, 'core/index.html', {'products': products_list})


def about(request):
    return render(request, 'core/about.html')
