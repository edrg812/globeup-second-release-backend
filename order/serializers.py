from rest_framework import serializers
from .models import Order, OrderItem
from product.models import ProductVariant
from user.models import User

class ProductVariantSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()  # custom display name

    class Meta:
        model = ProductVariant
        fields = ["id", "name", "price", "image", "sku"]

    def get_name(self, obj):
        parts = [obj.product.name]
        if obj.color:
            parts.append(obj.color)
        if obj.size:
            parts.append(obj.get_size_display())
        return " - ".join(parts)


class OrderItemSerializer(serializers.ModelSerializer):
    product_variant_id = serializers.PrimaryKeyRelatedField(
        queryset=ProductVariant.objects.all(),
        source="product_variant",
        write_only=True
    )
    product_variant = ProductVariantSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ["id", "product_variant", "product_variant_id", "quantity", "price"]
        read_only_fields = ["id", "price", "product_variant", "order"]


class OrderSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = "__all__"
        read_only_fields = ["id", "total_amount", "created_at", "user"]

    def create(self, validated_data):
        items_data = validated_data.pop("items", [])
        user = validated_data.pop("user", None)
        if not user:
            raise serializers.ValidationError("User is required")

        # Calculate total_amount
        total = 0
        for item_data in items_data:
            product_variant = item_data["product_variant"]
            quantity = item_data["quantity"]
            total += product_variant.price * quantity

        order = Order.objects.create(user=user, total_amount=total, **validated_data)

        # Create order items
        for item_data in items_data:
            OrderItem.objects.create(
                order=order,
                product_variant=item_data["product_variant"],
                quantity=item_data["quantity"],
                price=item_data["product_variant"].price
            )

        return order