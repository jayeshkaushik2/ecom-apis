from . import apis
from django.urls import path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"delivery_locations", apis.DeliveryLocationApi, basename="delivery_locations")

urlpatterns = [
    path("order/<str:ref>/", apis.orderApi, name="order"),
    path("place-order/<str:ref>/", apis.placeOrderApi, name="place-order"),
    path("order_address/<str:ref>/", apis.OrderAddressRefApi, name="order_address")
]

urlpatterns += router.urls