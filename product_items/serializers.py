from rest_framework import serializers
from .models import *


class Product_ImagesField(serializers.PrimaryKeyRelatedField):
    def get_queryset(self, *args, **kw):
        return Product_Images.objects.all()

class Product_ImagesSz(serializers.ModelSerializer):
    class Meta:
        model = Product_Images
        fields = (
            'id',
            'image',
            'product',
        )

class ProductSz(serializers.ModelSerializer):
    images = Product_ImagesSz(many=True, required=False)
    class Meta:
        model = Product
        fields = (
            'id',
            'sub_category',
            'title',
            'description',
            'is_promoted',
            'sorting_number',
            'price',
            'images',
        )