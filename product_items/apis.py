from rest_framework import viewsets
from .models import ProductImage, Product
from .serializers import Product_ImagesSz, ProductSz
from django.conf import settings
from django_filters import rest_framework as filters
from django.db.models import Q


class Product_ImageApi(viewsets.ModelViewSet):
    serializer_class = Product_ImagesSz

    def get_queryset(self):
        return ProductImage.objects.all()


class ProductFilter(filters.FilterSet):
    sub_category_or_title = filters.CharFilter(method="get_sub_category_or_title")

    def get_sub_category_or_title(self, queryset, value, *args, **kwargs):
        val = args[0]
        return queryset.filter(
            Q(sub_category__name__icontains=val) | Q(title__icontains=val)
        )

    class Meta:
        model = Product
        fields = {
            "sub_category__name": ("exact", "icontains"),
            "is_promoted": ("exact",),
            "title": ("exact", "icontains"),
            "price": ("lt", "gt", "lte", "gte"),
            "rating": ("lt", "gt", "lte", "gte"),
            "discount_pct": ("lt", "gt", "lte", "gte"),
            "tags__text": ("exact",),
        }


class ProductApi(viewsets.ModelViewSet):
    serializer_class = ProductSz
    filterset_class = ProductFilter

    def get_queryset(self):
        return Product.objects.all()
