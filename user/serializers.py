
# from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
# from djoser.serializers import UserSerializer as BaseUserSerializer
# from rest_framework import serializers
# from .models import User, UserProfile


# class UserProfileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = UserProfile
#         fields = [
#             "user_type",
#             "first_name",
#             "last_name",
#             "email",
#             "date_of_birth",
#             "gender",
#             "profile_image",
#             "default_shipping_address",
#             "default_billing_address",
#         ]


# class UserCreateSerializer(BaseUserCreateSerializer):
#     profile = UserProfileSerializer(required=False)

#     class Meta(BaseUserCreateSerializer.Meta):
#         model = User
#         fields = [
#             "id",
#             "phone_number",
#             "email",
#             "password",
#             "is_verified",
#             "profile",
#         ]
#         extra_kwargs = {
#             "password": {"write_only": True},
#             "is_verified": {"read_only": True},
#         }

#     def create(self, validated_data):
#         profile_data = validated_data.pop("profile", {})
#         user = super().create(validated_data)
#         UserProfile.objects.create(user=user, **profile_data)
#         return user


# class UserSerializer(BaseUserSerializer):
#     profile = UserProfileSerializer()

#     class Meta(BaseUserSerializer.Meta):
#         model = User
#         fields = [
#             "id",
#             "phone_number",
#             "email",
#             "is_verified",
#             "is_active",
#             "is_staff",
#             "date_joined",
#             "profile",
#         ]







from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from djoser.serializers import UserSerializer as BaseUserSerializer
from rest_framework import serializers
from .models import User, UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
  
    phone_number = serializers.CharField(source='user.phone_number', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    is_verified = serializers.BooleanField(source='user.is_verified', read_only=True)
    
    class Meta:
        model = UserProfile
        fields = [
            "id",
            "user_type",
            "first_name",
            "last_name",
            "phone_number",  # From User model
            "email",         # From User model
            "is_verified",   # From User model
            "date_of_birth",
            "gender",
            "profile_image",
            "default_shipping_address",
            "default_billing_address",
            "modified_at",
        ]

class UserCreateSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(required=False)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "phone_number",
            "email",
            "password",
            "is_verified",
            "profile",
        ]
        extra_kwargs = {
            "is_verified": {"read_only": True},
        }

    def create(self, validated_data):
        profile_data = validated_data.pop('profile', None)
        
        # Create user manually
        user = User.objects.create_user(
            phone_number=validated_data['phone_number'],
            email=validated_data.get('email'),
            password=validated_data['password']
        )
        
        # Create profile
        if profile_data:
            UserProfile.objects.create(user=user, **profile_data)
        else:
            UserProfile.objects.create(user=user)
        
        return user

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['profile'] = UserProfileSerializer(instance.profile).data
        return representation
class UserSerializer(BaseUserSerializer):
    profile = UserProfileSerializer(read_only=True)

    class Meta(BaseUserSerializer.Meta):
        model = User
        fields = [
            "id",
            "phone_number",
            "email",
            "is_verified",
            "is_active",
            "is_staff",
            "date_joined",
            "profile",
        ]



class ResellerSuplierRequestSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(source='user.phone_number', read_only=True)

    class Meta:
        model = UserProfile
        fields = [
            "id",
            "is_request",
            "request_for",
            "user_type",
            "user",
            "phone_number",
        ]
        read_only_fields = ("user",)   # prevent "User not found"






