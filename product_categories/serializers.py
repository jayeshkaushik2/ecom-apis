from rest_framework import serializers
from .models import Category, Sub_category


class CategorySz(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            'id',
            'name',
            'is_promoted',
            'sorting_number',
        )

class SubCategorySz(serializers.ModelSerializer):
    class Meta:
        model = Sub_category
        fields = (
            'id',
            'category',
            'name',
            'is_promoted',
            'sorting_number',
        )