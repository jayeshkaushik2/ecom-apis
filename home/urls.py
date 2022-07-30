from django.urls import path
from .views import ecom_details, homepage, homepage_ImageApi
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"homepage_images", homepage_ImageApi, basename="homepage_images")

urlpatterns = [
    path("details/", ecom_details, name="details"),
    path("homepage/", homepage, name="homepage"),
]

urlpatterns += router.urls
