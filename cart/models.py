from django.db import models
from user.models import User
from product.models import ProductVariant
from django.core.validators import MinValueValidator


class Cart(models.Model):
    """Shopping cart for users"""

    # id = models.CharField(max_length=255, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    def __str__(self):
        return f"Cart - {self.user.email}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    # product_id = models.ForeignKey(
    #     ProductVariant, on_delete=models.CASCADE, related_name="cart_items"
    # )
    quantity = models.PositiveIntegerField(default=1)

    """Items in shopping cart"""
    # id = models.CharField(max_length=255, primary_key=True)
    # cart = models.ForeignKey(Cart, on_delete=models.CASCADE, db_index=True, related_name='items')
    product_variant = models.ForeignKey(
        ProductVariant,
        on_delete=models.CASCADE,
        db_index=True,
        related_name="cart_item",
    )
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])

    class Meta:
        unique_together = ["cart", "product_variant"]

    # def __str__(self):
    #     return f"{self.cart.user.email} - {self.product_variant.sku} (x{self.quantity})"
