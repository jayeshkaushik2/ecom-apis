from . import apis
from django.urls import path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"delivery_locations", apis.DeliveryLocationApi, basename="delivery_locations")

urlpatterns = [
    path("order_update/", apis.orderApi, name="order_update")
]

urlpatterns += router.urls