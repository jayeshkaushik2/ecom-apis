from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSz(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "first_name",
            "last_name",
            "username",
            "email",
            "mobile",
            "date_joined",
            "last_login",
            "is_active",
            "is_admin",
            "is_staff",
            "is_manager",
            "is_superuser",
            "profile_image",
            "banner_image",
        )
        read_only_fields = (
            "date_joined",
            "last_login",
            "is_active",
            "is_admin",
            "is_staff",
            "is_manager",
            "is_superuser",
        )


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


class UserEmailSz(serializers.ModelSerializer):
    class Meta:
        model = UserEmail
        fields = (
            "id",
            "user",
            "email",
            "is_verified",
            "counter",
        )


class UserPhoneSz(serializers.ModelSerializer):
    class Meta:
        model = UserPhone
        fields = (
            "id",
            "user",
            "phone",
            "is_verified",
            "counter",
        )
