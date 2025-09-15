from .models import SellerSupplierCategory

from  rest_framework import serializers

class SellerSupplierCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model= SellerSupplierCategory
        fields="__all__"