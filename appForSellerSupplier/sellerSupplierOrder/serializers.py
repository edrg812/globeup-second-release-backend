from django.db import transaction
from rest_framework import serializers
from .models import SellerSupplierOrder, SellerSupplierOrderItem
from appForSellerSupplier.sellerSupplierProduct.models import (
    SellerSupplierProductVariant,
)
from earning.models import Earning


class SellerSupplierProductVariantSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = SellerSupplierProductVariant
        fields = ["id", "name", "price", "image", "sku"]

    def get_name(self, obj):
        parts = [obj.product.name]
        if obj.color:
            parts.append(obj.color)
        if obj.size:
            parts.append(obj.get_size_display())
        return " - ".join(parts)


class SellerSupplierOrderItemSerializer(serializers.ModelSerializer):
    product_variant_id = serializers.PrimaryKeyRelatedField(
        queryset=SellerSupplierProductVariant.objects.all(),
        source="product_variant",
        write_only=True,
    )
    product_variant = SellerSupplierProductVariantSerializer(read_only=True)

    class Meta:
        model = SellerSupplierOrderItem
        fields = [
            "id",
            "product_variant",
            "product_variant_id",
            "quantity",
            "price",
            "reselling_price",
        ]
        read_only_fields = ["id", "price", "product_variant", "order"]


# class SellerSupplierOrderSerializer(serializers.ModelSerializer):
#     user = serializers.StringRelatedField(read_only=True)
#     items = SellerSupplierOrderItemSerializer(many=True)

#     class Meta:
#         model = SellerSupplierOrder
#         fields = "__all__"
#         read_only_fields = ["id", "total_amount", "created_at", "user"]

#     def create(self, validated_data):
#         items_data = validated_data.pop("items", [])
#         user = validated_data.pop("user", None)
#         # user = self.context["request"].user  # get logged-in user

#         if not user:
#             raise serializers.ValidationError("User is required")

#         # Calculate total_amount
#         total = 0
#         for item_data in items_data:
#             product_variant = item_data["product_variant"]
#             quantity = item_data["quantity"]
#             total += product_variant.price * quantity

#         order = SellerSupplierOrder.objects.create(user=user, total_amount=total, **validated_data)

#         # Create order items
#         for item_data in items_data:
#             SellerSupplierOrderItem.objects.create(
#                 order=order,
#                 product_variant=item_data["product_variant"],
#                 quantity=item_data["quantity"],
#                 price=item_data["product_variant"].price
#             )

#         return order
    
#     def update(self, instance, validated_data):
#         old_status = instance.status
#         instance = super().update(instance, validated_data)

#         # ✅ When status changes to delivered
#         if old_status != "delivered" and instance.status == "delivered":
#             earning, _ = Earning.objects.get_or_create(user=instance.user)

#             # Move upcoming_balance → current_balance
#             if earning.upcoming_balance > 0:
#                 earning.current_balance += earning.upcoming_balance
#                 earning.upcoming_balance = 0
#                 earning.save()

#         return instance






class SellerSupplierOrderSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    items = SellerSupplierOrderItemSerializer(many=True)

    class Meta:
        model = SellerSupplierOrder
        fields = "__all__"
        read_only_fields = ["id", "total_amount", "created_at", "user"]

    # def create(self, validated_data):
    #     items_data = validated_data.pop("items", [])
    #     user = self.context["request"].user if "request" in self.context else None
    #     if not user:
    #         raise serializers.ValidationError("User is required")

    def create(self, validated_data):
         items_data = validated_data.pop("items", [])
         user = validated_data.pop("user", None)
         # user = self.context["request"].user  # get logged-in user

         if not user:
             raise serializers.ValidationError("User is required")

         # Calculate total_amount
         total = 0
         for item_data in items_data:
             product_variant = item_data["product_variant"]
             quantity = item_data["quantity"]
             total += product_variant.price * quantity
         order = SellerSupplierOrder.objects.create(user=user, total_amount=total, **validated_data)

         # Create order items
         for item_data in items_data:
             SellerSupplierOrderItem.objects.create(
                 order=order,
                 product_variant=item_data["product_variant"],
                 quantity=item_data["quantity"],
                 price=item_data["product_variant"].price,
                 reselling_price=item_data.get("reselling_price") or item_data["product_variant"].price

             )

         return order
    
    # def update(self, instance, validated_data):
    #      old_status = instance.status
    #      instance = super().update(instance, validated_data)

    #      # ✅ When status changes to delivered
    #      if old_status != "delivered" and instance.status == "delivered":
    #          earning, _ = Earning.objects.get_or_create(user=instance.user)

    #          # Move upcoming_balance → current_balance
    #         #  if earning.reseller_commission > 0:
    #         #      earning.current_balance += earning.upcoming_balance
    #         #      earning.upcoming_balance = 0
    #         #      earning.save()

    #      return instance
