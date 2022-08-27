from order import urls
from . import apis
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"addresses", apis.OrderAddressApi, basename="addresses")

urlpatterns = [
    path('token/', apis.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user-profile/', apis.CreateUserApi, name='user-profile'),
]

urlpatterns += router.urls