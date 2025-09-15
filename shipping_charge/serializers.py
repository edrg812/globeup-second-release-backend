from .models import ShippingCharge
from rest_framework import serializers

class ShippingChargeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingCharge
        fields = "__all__"
