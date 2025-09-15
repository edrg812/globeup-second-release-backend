from rest_framework import serializers
from .models import WithdrawRequestByReseller

# class WithdrawRequestByResellerSerializer(serializers.ModelSerializer):
#     user = serializers.StringRelatedField(read_only=True)  # shows user phone_number or __str__
    
#     class Meta:
#         model = WithdrawRequestByReseller
#         fields = [
#             'id',
#             'user',
#             'amount',
#             'payment_method',
#             'account_details',
#             'requested_at',
#             'processed',
#             'processed_at'
#         ]
#         read_only_fields = ['id', 'user', 'requested_at', 'processed', 'processed_at']



class WithdrawRequestByResellerSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = WithdrawRequestByReseller
        fields = [
            'id', 'user', 'amount', 'payment_method', 
            'account_details', 'requested_at', 'processed', 'processed_at'
        ]
        read_only_fields = ['id', 'user', 'requested_at', 'processed_at']

    def validate(self, attrs):
        user = self.context['request'].user
        if WithdrawRequestByReseller.objects.filter(user=user, processed=False).exists():
            raise serializers.ValidationError("You already have a pending withdrawal request.")
        return attrs


#this serializer will be included in the earing serializer so that admin can get "payment_method and account_details "
class WithdrawRequestByResellerSerializerTobeIncludedEarning(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = WithdrawRequestByReseller
        fields = [
            'id', 'user', 'amount', 'payment_method', 
            'account_details', 'requested_at', 'processed', 'processed_at'
        ]
        read_only_fields = ['id', 'user', 'requested_at', 'processed_at']

    
