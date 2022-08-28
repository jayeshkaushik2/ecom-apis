from rest_framework import serializers
from .models import *


class ProfileSz(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = (
            "id",
            "name",
            "user",
            "profile_image",
            "banner_image",
        )


class AddressSz(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = (
            "id",
            "user",
            "full_name",
            "phone",
            "alternate_phone",
            "pincode",
            "city",
            "area_info",
            "house_info",
            "state",
            "ref",
        )
