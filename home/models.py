from django.db import models
from django.conf import settings
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.
class Homepage_Images(models.Model):
    homepage = models.ForeignKey(
        settings.HOMEPAGE_MODEL, on_delete=models.CASCADE, related_name="images"
    )
    image = models.ImageField(upload_to="homepage_image/")
    sorting_number = models.PositiveBigIntegerField(null=True, blank=True)
    is_dark = models.BooleanField(default=False)


class Homepage(models.Model):
    title = models.CharField(max_length=300, null=True, blank=True)
    description = models.TextField(null=True, blank=True)


class Founder(models.Model):
    detail = models.ForeignKey(
        settings.DETAIL_MODEL, on_delete=models.CASCADE, related_name="founders"
    )
    is_head = models.BooleanField(default=False)
    name = models.CharField(max_length=300, null=True, blank=True)
    profession = models.CharField(max_length=300, null=True, blank=True)

class Detail(models.Model):
    contact = PhoneNumberField(null=True, blank=True)
    alternate1_contact = PhoneNumberField(null=True, blank=True)
    alternate2_contact = PhoneNumberField(null=True, blank=True)
    email = models.CharField(max_length=300, null=True, blank=True)
    about_us = models.TextField(null=True, blank=True)
    logo = models.ImageField(upload_to="logos/", null=True, blank=True)
    instagram_link = models.CharField(max_length=500, null=True, blank=True)
    facebook_link = models.CharField(max_length=500, null=True, blank=True)
    twitter_link = models.CharField(max_length=500, null=True, blank=True)
    youtube_link = models.CharField(max_length=500, null=True, blank=True)
