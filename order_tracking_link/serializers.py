from rest_framework import serializers
from .models import CustomerOrderTrackingLink, ResellerOrderTrackingLink

class CustomerOrderTrackingSerializer(serializers.ModelSerializer):
    class Meta:
        model=CustomerOrderTrackingLink
        fields=["tracking_link", "order_model"]

class ResellerOrderTrackingSerializer(serializers.ModelSerializer):
    class Meta:
        model=ResellerOrderTrackingLink
        fields=["tracking_link", "order_model"]