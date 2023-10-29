from django.contrib import admin
from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.contrib import messages

from .models import Color, Category, Product, ProductVariant, Supplier, ProductImage
from .widgets import MultiFileInput


class AdminProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        widgets = {'image': MultiFileInput}
        fields = '__all__'


class AdminProductImage(admin.ModelAdmin):
    form = AdminProductImageForm

    def add_view(self, request, form_url="", extra_context=None, *args, **kwargs):
        images = request.FILES.getlist('image', [])
        is_valid = self.form(request.POST, request.FILES).is_valid()

        if request.method == 'GET' or len(images) <= 1 or not is_valid:
            return super(AdminProductImage, self).add_view(request, *args, **kwargs)

        product = ProductVariant.objects.get(pk=int(request.POST['product']))
        for image in images:
            try:
                img = ProductImage(product=product, image=image)
                img.save()
            except Exception as e:
                messages.error(request, e)

        return HttpResponseRedirect('admin/products/productimag/')


class AdminProductVariantForm(forms.ModelForm):
    class Meta:
        model = ProductVariant
        fields = '__all__'


class AdminInlineProductVariant(admin.TabularInline):
    model = ProductVariant
    form = AdminProductVariantForm
    extra = 1


class AdminProduct(admin.ModelAdmin):
    inlines = [AdminInlineProductVariant]


admin.site.register(Product, AdminProduct)
admin.site.register(ProductImage, AdminProductImage)
admin.site.register(Category)
admin.site.register(Supplier)
admin.site.register(Color)
