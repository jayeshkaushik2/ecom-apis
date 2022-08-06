from . import views
from django.urls import path

urlpatterns = [
    path('create_cart/', views.create_cart, name='create_cart'),
    path('update_cart/<str:ref>/', views.update_cart, name='update_cart'),
]