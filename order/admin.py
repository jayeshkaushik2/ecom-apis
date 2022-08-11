from django.contrib import admin
from .models import DeliveryLocation, Order


# Register your models here.
admin.site.register(DeliveryLocation)
admin.site.register(Order)