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
            "created_at",
            "received_at",
            "out_for_delivery_at",
            "completed_at",
            "returned_at",
            "exchange_at",
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
