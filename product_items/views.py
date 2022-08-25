from rest_framework import viewsets
from .models import ProductImage, Product
from .serializers import Product_ImagesSz, ProductSz
from django.conf import settings
from django_filters import rest_framework as filters


# Create your views here.
class Product_ImageApi(viewsets.ModelViewSet):
    serializer_class = Product_ImagesSz

    def get_queryset(self):
        return ProductImage.objects.all()


class ProductFilter(filters.FilterSet):
    class Meta:
        model = Product
        fields = {
            "sub_category__name": ("exact", ),
            "is_promoted": ("exact", ),
            "title": ("exact", ),
            "price": ("lt", "gt", "lte", "gte"),
        }

class ProductApi(viewsets.ModelViewSet):
    serializer_class = ProductSz
    filterset_class = ProductFilter

    def get_queryset(self):
        return Product.objects.all()