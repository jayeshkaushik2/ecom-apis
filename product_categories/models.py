from django.db import models

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

    def __str__(self) -> str:
        return self.name