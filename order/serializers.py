from rest_framework import serializers
from .models import DeliveryLocation, Order


class OrderSz(serializers.ModelSerializer):
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
            "total_price",
            "total_discount",
        )


class DeliveryLocationSz(serializers.ModelSerializer):
    class Meta:
        model = DeliveryLocation
        fields = (
            "id",
            "pincode",
            "pickup_charge",
            "delivery_charge",
            "is_active",
        )
