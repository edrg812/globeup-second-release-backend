from django.contrib import admin

# Register your models here.
from .models import SellerSupplierProduct, SellerSupplierProductVariant

class SellerSupplierProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'created_at')
    search_fields = ('name', 'description')

class SellerSupplierProductVariantAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'color', 'size', 'price', 'sku')
    list_filter = ('color', 'size')
    search_fields = ('product__name', 'sku')
admin.site.register(SellerSupplierProduct, SellerSupplierProductAdmin)
admin.site.register(SellerSupplierProductVariant, SellerSupplierProductVariantAdmin)