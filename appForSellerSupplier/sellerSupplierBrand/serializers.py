from .models import SellerSupplierBrand
from  rest_framework import serializers

class SellerSupplierBrandSerializer(serializers.ModelSerializer):
    class Meta:
        model= SellerSupplierBrand
        fields="__all__"