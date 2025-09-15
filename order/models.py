from django.db import models
from user.models import User
from product.models import ProductVariant
from django.core.validators import MinValueValidator

class Order(models.Model):
    """Customer orders"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    
    # id = models.CharField(max_length=255, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', db_index=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, db_index=True)
    shipping_address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    customer_name_orderedby_admin=models.CharField(max_length=20,blank=True, null=True)
    customer_phone_orderedby_admin=models.CharField(max_length=20, blank=True, null=True)



    
   

class OrderItem(models.Model):
    """Items in an order"""
   
    order = models.ForeignKey(Order, on_delete=models.CASCADE, db_index=True, related_name='items')
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, db_index=True)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    price = models.DecimalField(max_digits=10, decimal_places=2, db_index=True)

