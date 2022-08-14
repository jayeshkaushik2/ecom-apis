from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.
class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=256, null=True, blank=True)
    profile_image = models.ImageField(null=True, blank=True)
    banner_image = models.ImageField(null=True, blank=True)

    def __str__(self) -> str:
        return self.name


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=256, null=True, blank=True)
    phone = PhoneNumberField(null=True, blank=True)
    alternate_phone = PhoneNumberField(null=True, blank=True)
    pincode = models.CharField(max_length=256, null=True, blank=True)
    city = models.CharField(max_length=256, null=True, blank=True)
    area_info = models.TextField(null=True, blank=True)
    house_info = models.TextField(null=True, blank=True)
    state = models.CharField(max_length=256, null=True, blank=True)
