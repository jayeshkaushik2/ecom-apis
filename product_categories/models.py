from django.db import models
from common.ImageThumbCovert import image_to_thumb

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=256, null=True, blank=True)
    is_promoted = models.BooleanField(default=False)
    sorting_number = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self) -> str:
        return self.name


class Sub_category(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=256, null=True, blank=True)
    is_promoted = models.BooleanField(default=False)
    sorting_number = models.PositiveIntegerField(null=True, blank=True)
    image = models.ImageField(upload_to="sub_categories/", null=True, blank=True)
    thumb = models.ImageField(upload_to="sub_categories/", null=True, blank=True)

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs) -> None:
        if self.thumb is None or self.thumb == "":
            image_to_thumb(obj=self, image_name="image")
            self.updated = True
        return super().save(*args, **kwargs)
