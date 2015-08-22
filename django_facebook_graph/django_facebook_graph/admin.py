from django.contrib import admin

from .models import *

class ProductAdmin(admin.ModelAdmin):
    list_filter = ['name']


class TransactionAdmin(admin.ModelAdmin):
    pass

admin.site.register(Product, ProductAdmin)
admin.site.register(Transaction, TransactionAdmin)
