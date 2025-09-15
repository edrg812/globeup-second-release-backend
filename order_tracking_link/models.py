from django.db import models
from order.models import Order
from appForSellerSupplier.sellerSupplierOrder.models import SellerSupplierOrder




class CustomerOrderTrackingLink(models.Model):
    order_model= models.OneToOneField(Order, related_name="tracking_link", on_delete=models.CASCADE)
    tracking_link=models.URLField(max_length=2083, unique=True)
    created_at= models.DateTimeField(auto_now_add=True)
    modified_at= models.DateTimeField(auto_now=True)


class ResellerOrderTrackingLink(models.Model):
    order_model= models.OneToOneField(SellerSupplierOrder, related_name="tracking_link", on_delete=models.CASCADE)
    tracking_link=models.URLField(max_length=2083, unique=True)
    created_at= models.DateTimeField(auto_now_add=True)
    modified_at= models.DateTimeField(auto_now=True)

