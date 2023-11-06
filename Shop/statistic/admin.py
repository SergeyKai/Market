from django.contrib import admin

from .models import Sale, Revenue, Expense

admin.site.register(Sale)
admin.site.register(Revenue)
admin.site.register(Expense)
