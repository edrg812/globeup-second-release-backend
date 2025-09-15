from rest_framework import serializers
from .models import SiteSetting


class SiteSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteSetting
        fields = ["id", "site_name", "white_logo", "dark_logo", "favicon", "status"]
