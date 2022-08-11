import json
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Cart, CartLine
from .serializers import CartSz, CartRefSz, CartDataSz


# Create your views here.
@api_view(["GET"])
def create_cartApi(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        cart = Cart.objects.create()
    sz = CartRefSz(instance=cart)
    return Response(sz.data)


@api_view(["GET", "POST", "DELETE"])
def update_cartApi(request, ref):
    user = None
    if request.user.is_authenticated:
        user = request.user
    if request.method == "GET":
        cart = Cart.objects.filter(ref=ref, user=user, status="open").first()
        if cart is not None:
            sz = CartSz(instance=cart)
            return Response(sz.data)
        return Response({"errors": ["cart does not exists"]}, status=404)
    elif request.method == "POST":
        cart = Cart.objects.filter(ref=ref).first()
        if cart is not None:
            sz = CartDataSz(instance=cart, data=request.data, partial=True)
            if sz.is_valid(raise_exception=True):
                sz.save()
                return Response(sz.data)
        return Response({"errors": ["cart does not exists"]}, status=404)
    else:
        line_ids = request.data.get("line_ids", [])
        for line_id in line_ids:
            line = CartLine.objects.filter(id=int(line_id)).first()
            if line is not None:
                line.delete()
        
        return Response({"msg":["deleted successfully"]}, status=204)
