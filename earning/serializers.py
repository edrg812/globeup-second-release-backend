from rest_framework import serializers
from .models import Earning


class EarningSerializer(serializers.ModelSerializer):
    class Meta:
        model = Earning
        fields = "__all__"
        read_only_fields = (
            "user",
            "current_balance",
            "total_sales_balance",
            "pending_payout",
            "completed_payout",
            "status",
            "created_at",
            "updated_at",
        )

class EarningStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Earning
        fields = "__all__"
        read_only_fields = (
            "user",
            "current_balance",
            "total_sales_balance",
            "pending_payout",
            "completed_payout",
            # "status",
            "created_at",
            "updated_at",
        )


class WithdrawRequestSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Withdrawal amount must be greater than 0.")
        return value




#serializer for admin to see all withdraw requests
from rest_framework import serializers
from .models import Earning
from payment.serializers import WithdrawRequestByResellerSerializerTobeIncludedEarning

class EarningAdminSerializer(serializers.ModelSerializer):
    user_phone = serializers.CharField(source="user.phone_number", read_only=True)
    method_detail = WithdrawRequestByResellerSerializerTobeIncludedEarning(
        many=True,
        source="user.withdraw_requests"  # <--- this must be a string
    )
    class Meta:
        model = Earning
        fields = [
            "id",
            "user",
            "user_phone",
            "current_balance",
            "total_sales_balance",
            "pending_payout",
            "completed_payout",
            # "reseller_commission",
            "commission_percent",
            "user_requested_amount_withdraw",
            "status",
            "created_at",
            "updated_at",
            "method_detail"
        ]
        read_only_fields = ("created_at", "updated_at", "user_phone")
