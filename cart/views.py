from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Cart
from .serializers import CartSz

# Create your views here.
@api_view(["GET"])
def create_cart(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        cart = Cart.objects.create()
    sz = CartSz(instance=cart)
    return Response(sz.data)


@api_view(["GET", "POST", "DELETE"])
def update_cart(request, ref):
    if request.method == "GET":
        return Response({"success":True})
    elif request.method == "POST":
        pass
    else:
        pass