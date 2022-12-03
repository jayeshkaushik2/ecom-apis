from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user_model
from order.models import Order
from django.conf import settings
import os

User = get_user_model()


class UserSz(serializers.ModelSerializer):
    profile_image = serializers.ImageField(
        max_length=None, use_url=True, allow_null=True, required=False
    )
    banner_image = serializers.ImageField(
        max_length=None, use_url=True, allow_null=True, required=False
    )

    class Meta:
        model = User
        fields = (
            "id",
            "first_name",
            "last_name",
            "username",
            "email",
            "mobile",
            "date_joined",
            "last_login",
            "is_active",
            "is_admin",
            "is_staff",
            "is_manager",
            "is_superuser",
            "profile_image",
            "banner_image",
        )
        read_only_fields = (
            "date_joined",
            "last_login",
            "is_active",
            "is_admin",
            "is_staff",
            "is_manager",
            "is_superuser",
        )


class ProfileSz(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = (
            "id",
            "name",
            "user",
            "profile_image",
            "banner_image",
        )


class AddressSz(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = (
            "id",
            "user",
            "full_name",
            "phone",
            "alternate_phone",
            "pincode",
            "city",
            "area_info",
            "house_info",
            "state",
            "ref",
        )


class UserEmailSz(serializers.ModelSerializer):
    class Meta:
        model = UserEmail
        fields = (
            "id",
            "user",
            "email",
            "is_verified",
            "counter",
        )


class UserPhoneSz(serializers.ModelSerializer):
    class Meta:
        model = UserPhone
        fields = (
            "id",
            "user",
            "phone",
            "is_verified",
            "counter",
        )


from cart.serializers import CartDataSz


class UserOrderSz(serializers.ModelSerializer):
    cart = serializers.SerializerMethodField(method_name="get_cart_details")

    class Meta:
        model = Order
        fields = (
            "id",
            "user",
            "cart",
            "address",
            "ref",
            "order_type",
            "order_status",
            "payment_method",
            "created_at",
            "received_at",
            "out_for_delivery_at",
            "completed_at",
            "returned_at",
            "exchange_at",
            "total_price",
            "total_discount",
        )
        read_only_fields = (
            "cart",
            "address",
            "ref",
            "order_type",
            "order_status",
            "payment_method",
            "created_at",
            "received_at",
            "out_for_delivery_at",
            "completed_at",
            "returned_at",
            "exchange_at",
            "total_price",
            "total_discount",
        )

    def get_cart_details(self, obj):
        cart = obj.cart
        data = CartDataSz(cart)
        return data.data
