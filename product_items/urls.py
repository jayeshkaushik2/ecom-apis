from django.urls import path
from .views import ProductApi, Product_ImageApi
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"product", ProductApi, basename="product")
router.register(r"product_image", Product_ImageApi, basename="product_image")

urlpatterns = [
]

urlpatterns += router.urls