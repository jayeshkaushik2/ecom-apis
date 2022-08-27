from rest_framework import viewsets
from django_filters import rest_framework as filters
from .models import Category, Sub_category
from .serializers import CategorySz, SubCategorySz


class CategoryFilter(filters.FilterSet):
    class Meta:
        model = Category
        fields = {
            "is_promoted": ("exact", ),
            "name": ("exact", ),
        }

class CategoriesApi(viewsets.ModelViewSet):
    serializer_class = CategorySz 
    filterset_class = CategoryFilter

    def get_queryset(self):
        return Category.objects.all()



class Sub_categoryFilter(filters.FilterSet):
    class Meta:
        model = Sub_category
        fields = {
            "is_promoted": ("exact", ),
            "name": ("exact", ),
        }

class Sub_CategoriesApi(viewsets.ModelViewSet):
    serializer_class = SubCategorySz 
    filterset_class = Sub_categoryFilter

    def get_queryset(self):
        return Sub_category.objects.all()