
from django.apps import AppConfig

class SellerSupplierOrderConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'appForSellerSupplier.sellerSupplierOrder'
    label = 'seller_supplier_order_unique'  # <--- unique label


    def ready(self):
        import appForSellerSupplier.sellerSupplierOrder.signals  # register signals





