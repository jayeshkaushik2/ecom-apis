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


class CartRefSz(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ("id", "ref")


class CartSz(serializers.ModelSerializer):
    lines = CartLineSz(many=True, required=False)

    class Meta:
        model = Cart
        fields = (
            "id",
            "user",
            "ref",
            "lines",
        )

    def create(self, validated_data):
        lines = validated_data.pop("lines", None)
        cart = Cart.objects.create(**validated_data)
        for line in lines:
            created_line = CartLine.objects.create(**line)
            created_line.set_price()
            cart.lines.add(created_line)
        return cart

    def update(self, instance, validated_data):
        lines = validated_data.pop("lines", None)
        for line in lines:
            created_line = CartLine.objects.filter(**line).first()
            if created_line is not None:
                created_line.quantity += 1
                created_line.save()
                created_line.set_price()
            else:
                created_line = CartLine.objects.create(**line)
                created_line.set_price()
            instance.lines.add(created_line)
        return instance
