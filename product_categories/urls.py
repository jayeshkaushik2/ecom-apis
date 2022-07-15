from django.urls import path
from .views import CategoriesApi, Sub_CategoriesApi
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"category", CategoriesApi, basename="category")
router.register(r"sub_category", Sub_CategoriesApi, basename="sub_category")

urlpatterns = [
]

urlpatterns += router.urls