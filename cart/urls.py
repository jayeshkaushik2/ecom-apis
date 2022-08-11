from . import views
from django.urls import path

urlpatterns = [
    path('create_cart/', views.create_cartApi, name='create_cart'),
    path('update_cart/<str:ref>/', views.update_cartApi, name='update_cart'),
]