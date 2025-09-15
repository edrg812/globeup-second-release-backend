from django.db import models

# Create your models here.
from django.db import models
from user.models import User

# from product.models import ProductVariant
from appForSellerSupplier.sellerSupplierProduct.models import (
    SellerSupplierProductVariant,
)
from django.core.validators import MinValueValidator


class SellerSupplierOrder(models.Model):
    """Customer orders"""

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("processing", "Processing"),
        ("shipped", "Shipped"),
        ("delivered", "Delivered"),
        ("cancelled", "Cancelled"),
    ]

    # id = models.CharField(max_length=255, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="pending", db_index=True
    )
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, db_index=True)
    shipping_address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    customer_name = models.CharField(max_length=20, blank=True, null=True)
    customer_phone = models.CharField(max_length=20, blank=True, null=True)
    wholeSale_price = models.DecimalField(
        max_digits=10, decimal_places=2, db_index=True, blank=True, null=True
    )
    reselling_price = models.DecimalField(
        max_digits=10, decimal_places=2, db_index=True, blank=True, null=True
    )


class SellerSupplierOrderItem(models.Model):
    order = models.ForeignKey(
        SellerSupplierOrder, related_name="items", on_delete=models.CASCADE
    )
    product_variant = models.ForeignKey(
        SellerSupplierProductVariant, on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    reselling_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
