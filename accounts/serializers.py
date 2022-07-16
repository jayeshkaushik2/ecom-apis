from rest_framework import serializers
from .models import *

class ProfileSz(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = (
            "id",
            "name",
            "user",
        )