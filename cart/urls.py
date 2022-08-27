from . import apis
from django.urls import path

urlpatterns = [
    path('create_cart/', apis.create_cartApi, name='create_cart'),
    path('update_cart/<str:ref>/', apis.update_cartApi, name='update_cart'),
]