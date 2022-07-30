from rest_framework import serializers
from .models import *

class FounderSz(serializers.ModelSerializer):
    class Meta:
        model = Founder
        fields = (
            "id",
            "detail",
            "is_head",
            "name",
            "profession",
        )


class DetailSz(serializers.ModelSerializer):
    founders = FounderSz(many=True, required=False)
    class Meta:
        model = Detail
        fields = (
            "id",
            "contact",
            "alternate1_contact",
            "alternate2_contact",
            "email",
            "about_us",
            "logo",
            "instagram_link",
            "facebook_link",
            "twitter_link",
            "youtube_link",
            "founders",
        )


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
