from django.contrib import admin
from .models import Product, ProductVariant
# Register your models here.

class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'size', 'price', 'stock')

class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug', 'category', 'created_at', "brand", "description","is_active")

admin.site.register(ProductVariant, ProductVariantAdmin)
admin.site.register(Product, ProductAdmin)

