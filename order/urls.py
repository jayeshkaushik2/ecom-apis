from . import views
from django.urls import path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"delivery_locations", views.DeliveryLocationApi, basename="delivery_locations")

urlpatterns = [
    path("order_update/", views.orderApi, name="order_update")
]

urlpatterns += router.urls