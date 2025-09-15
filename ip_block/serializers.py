from rest_framework import serializers
from .models import IPBlock


class IPBlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = IPBlock
        fields = [
            "id",
            "ip_number",
            "reason",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]
