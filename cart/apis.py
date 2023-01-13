import json
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Cart, CartLine
from .serializers import CartSz, CartRefSz, CartDataSz


@api_view(["GET"])
def create_cartApi(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(
            user=request.user, status=Cart.Status.open
        )
    else:
        cart = Cart.objects.create()
    sz = CartRefSz(instance=cart)
    return Response(sz.data)


@api_view(["GET", "POST", "DELETE"])
def update_cartApi(request, ref):
    kw = {}
    kw["ref"] = ref
    user = None
    cart = Cart.objects.filter(**kw).first()
    if request.user.is_authenticated:
        kw["user"] = request.user
        user = request.user
    if cart is None:
        return Response({"errors": ["cart does not exists"]}, status=404)

    if cart.user is None:
        cart.user = user
        cart.save()
        
    if cart.status == Cart.Status.submitted:
        return Response({"error": ["cart is submitted"]}, status=404)

    if request.method == "GET":
        sz = CartSz(instance=cart)
        return Response(sz.data)

    elif request.method == "POST":
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

        return Response({"msg": ["deleted successfully"]}, status=204)
