from django.db import models
from user.models import User

from appForSellerSupplier.sellerSupplierCategory.models import SellerSupplierCategory
from appForSellerSupplier.sellerSupplierBrand.models import SellerSupplierBrand
from django.core.validators import MinValueValidator
from decimal import Decimal

class SellerSupplierProduct(models.Model):
    """Main product model"""
    # id = models.CharField(max_length=255, primary_key=True)
    user= models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)  # Seller or Supplier who added the product
    name = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)
    category = models.ForeignKey(SellerSupplierCategory, on_delete=models.CASCADE, db_index=True)
    brand = models.ForeignKey(SellerSupplierBrand, on_delete=models.CASCADE, db_index=True)
    description = models.TextField()
    is_active = models.BooleanField(default=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    # image = models.ImageField(upload_to='products/', default = "products/appleWatch_9U1DYxm.jpeg")
    # product_price = models.DecimalField(max_digits=10, decimal_places=2, db_index=True, default=1000)
    
    def __str__(self):
        return self.name

class SellerSupplierProductVariant(models.Model):
    """Product variants with different attributes like size, color"""
    SIZE_CHOICES = [
        ('s', 'Small'),
        ('m', 'Medium'),
        ('l', 'Large'),
        ('xl', 'Extra Large'),
        ('xxl', 'Double Extra Large'),
    ]
    
    # id = models.CharField(max_length=255, primary_key=True)
    product = models.ForeignKey(SellerSupplierProduct, on_delete=models.CASCADE, db_index=True, related_name='variants')
    sku = models.CharField(max_length=100, unique=True, db_index=True)
    old_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, db_index=True)
    stock = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    color = models.CharField(max_length=50, db_index=True, null=True, blank=True)
    size = models.CharField(max_length=3, choices=SIZE_CHOICES, null=True, blank=True)
    is_active = models.BooleanField(default=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True, db_index=True)
    image  = models.ImageField(upload_to='products/', null=True, blank=True)

    




from django.db import models

# Create your models here.
