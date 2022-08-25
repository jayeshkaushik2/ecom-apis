from rest_framework import serializers
from .models import ProductImage, ProductTag, Product


class Product_ImagesField(serializers.PrimaryKeyRelatedField):
    def get_queryset(self, *args, **kw):
        return ProductImage.objects.all()


class Product_ImagesSz(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = (
            "id",
            "image",
            "product",
        )


class ProductTagSz(serializers.ModelSerializer):
    class Meta:
        model = ProductTag
        fields = (
            "id",
            "text",
            "product",
        )


class ProductSz(serializers.ModelSerializer):
    images = Product_ImagesSz(many=True, required=False)
    tags = ProductTagSz(many=True, required=False)

    class Meta:
        model = Product
        fields = (
            "id",
            "sub_category",
            "title",
            "description",
            "is_promoted",
            "sorting_number",
            "price",
            "images",
            "rating",
            "discount_pct",
            "tags",
        )
