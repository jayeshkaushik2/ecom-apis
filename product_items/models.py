from unicodedata import name
from django.db import models
from product_categories.models import Sub_category
from django.conf import settings
# Create your models here.

class Product_Images(models.Model):
    product = models.ForeignKey(settings.PRODUCT_MODEL, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to='product_image/')
    is_primary = models.BooleanField(default=False)

class Product(models.Model):
    sub_category = models.ForeignKey(Sub_category, on_delete=models.CASCADE)
    title = models.CharField(max_length=256, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    is_promoted = models.BooleanField(default=False)
    sorting_number = models.PositiveIntegerField(null=True, blank=True)
    price = models.PositiveIntegerField(null=True, blank=True)
    rating = models.PositiveIntegerField(null=True, blank=True)
    discount_pct = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=2)


    def __str__(self) -> str:
        return self.title