from rest_framework import serializers
from .models import *


class CartLineSz(serializers.ModelSerializer):
    class Meta:
        model = CartLine
        fields = (
            "id",
            "product",
            "ref",
            "cart",
            "quantity",
            "discount",
            "price",
        )


class CartSz(serializers.ModelSerializer):
    cart_lines = CartLineSz(many=True, required=False)
    class Meta:
        model = Cart
        fields = (
            "id",
            "user",
            "ref",
            "cart_lines",
        )