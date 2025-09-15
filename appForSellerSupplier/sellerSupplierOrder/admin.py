from django.contrib import admin

# Register your models here.
from .models import SellerSupplierOrder, SellerSupplierOrderItem

class SellerSupplierOrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_amount', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'user__email')

class SellerSupplierOrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'product_variant', 'quantity', 'price')
    search_fields = ('order__id', 'product_variant__name')
admin.site.register(SellerSupplierOrder, SellerSupplierOrderAdmin)
admin.site.register(SellerSupplierOrderItem, SellerSupplierOrderItemAdmin)