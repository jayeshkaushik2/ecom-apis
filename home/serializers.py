from dataclasses import fields
from rest_framework import serializers
from .models import *


class DetailSz(serializers.ModelSerializer):
    class Meta:
        model = Detail
        fields = "__all__"


class Homepage_ImagesSz(serializers.ModelSerializer):
    class Meta:
        model = Homepage_Images
        fields = (
            "id",
            "homepage",
            "image",
            "sorting_number",
        )


class HomepageSz(serializers.ModelSerializer):
    images = Homepage_ImagesSz(many=True, required=False)
    class Meta:
        model = Homepage
        fields = (
            "id",
            "images",
            "title",
            "description",
        )
