from rest_framework import serializers

from .models import SellerSupplierProduct, SellerSupplierProductVariant
from review.models import Review
from appForSellerSupplier.sellerSupplierCategory.models  import SellerSupplierCategory
from appForSellerSupplier.sellerSupplierBrand.models import SellerSupplierBrand



class ProductSimpleSerializer(serializers.ModelSerializer):
    """Lightweight product serializer for nesting inside variants"""
    category = serializers.StringRelatedField()  # show category name instead of id
    brand = serializers.StringRelatedField()     # show brand name instead of id

    class Meta:
        model = SellerSupplierProduct
        fields = ["id", "name", "slug", "category", "brand", "description", "is_active"]



class SellerSupplierProductVariantSerializer(serializers.ModelSerializer):
    product = ProductSimpleSerializer(read_only=True)  # use simplified product

    class Meta:
        model = SellerSupplierProductVariant
        fields = "__all__"
        read_only_fields = ["id"]


class SellerSupplierProductSerializer(serializers.ModelSerializer):
    variants = SellerSupplierProductVariantSerializer(many=True, read_only=True)
    category = serializers.StringRelatedField()  # optional: show name instead of id
    brand = serializers.StringRelatedField()

    class Meta:
        model = SellerSupplierProduct
        fields = ["id", "name", "slug", "category", "brand", "description", "is_active", "variants"]
        read_only_fields = ["id"]



class ProductCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for creating/updating product only"""

    class Meta:
        model = SellerSupplierProduct
        fields = ["id", "name", "slug", "category", "brand", "description", "is_active"]
        read_only_fields = ["id"]


class ProductVariantCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for creating/updating product variants"""

    class Meta:
        model = SellerSupplierProductVariant
        fields = [
            "id",
            "product",
            "sku",
            "old_price",
            "price",
            "stock",
            "color",
            "size",
            "is_active",
            "image",
        ]
        read_only_fields = ["id"]



class PriceEditSerializer(serializers.ModelSerializer):
    class Meta:
        model= SellerSupplierProductVariant
        fields=["old_price","price","id"]

