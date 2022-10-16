from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, exceptions

from accounts.models import Address
from accounts.serializers import AddressSz

from .models import Order, DeliveryLocation
from .serializers import OrderSz, DeliveryLocationSz
from cart.models import Cart


class DeliveryLocationApi(viewsets.ModelViewSet):
    serializer_class = DeliveryLocationSz

    def get_queryset(self):
        return DeliveryLocation.objects.all()

    def check_location(self, pincode):
        check = DeliveryLocation.objects.filter(pincode, is_active=True).first()
        if check is not None:
            return Response({"success": True})
        return Response({"success": False})


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def OrderAddressRefApi(request, ref):
    kw = {}
    kw["ref"] = ref
    kw["user"] = request.user
    address = Address.objects.filter(**kw).first()
    if request.method == "GET":
        sz = AddressSz(instance=address)
        return Response(sz.data)
    else:
        sz = AddressSz(instance=address, data=request.data, partial=True)
        if sz.is_valid(raise_exception=True):
            sz.save()
            return Response(sz.data)


def check_order_address(order, address, data):
    if order is not None and order.address is None:
        order.address = address
        order.save()


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def orderApi(request, ref):
    kw = {}
    kw["ref"] = ref
    kw["user"] = request.user
    order = Order.objects.filter(**kw).first()
    address, created = Address.objects.get_or_create(**kw)
    check_order_address(order=order, address=address, data=request.data)
    if order is not None and order.order_status not in [Order.OrderStatus.pending]:
        return Response({"error": ["Order is already placed"]}, status=400)

    if request.method == "GET":
        if order is None:
            cart = Cart.objects.filter(**kw).first()
            if cart is None:
                raise Exception("Cart is None cannot create order")
            kw["cart"] = cart
            order = Order.objects.create(**kw)
            # trying setting order address if provided
            order.set_order_address()
            order.save()
            # checking if order price can be updated
            can_be_updated, msg = order.can_orderprice_be_updated()
            if not can_be_updated:
                return Response({"error": [msg]})
        # updating order price
        order.update_order_price()
        order.save()
        sz = OrderSz(instance=order)
        return Response(sz.data)
    else:
        data = request.data
        can_be_updated, msg = order.can_orderprice_be_updated()
        if not can_be_updated:
            return Response({"error": [msg]})
        sz = OrderSz(instance=order, data=data, partial=True)
        if sz.is_valid(raise_exception=True):
            order.update_order_price()
            sz.save()
            return Response(sz.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def placeOrderApi(request, ref):
    kw = {}
    kw["ref"] = ref
    kw["user"] = request.user
    cart = Cart.objects.filter(**kw).first()
    if cart is None:
        return Response({"error": ["cart not present"]}, status=400)

    kw["cart"] = cart
    order = Order.objects.filter(**kw).first()
    if order is None:
        return Response({"error": ["order not present"]}, status=400)

    can_be_placed, msg = order.can_be_placed()
    if not can_be_placed:
        return Response({"error": [msg]}, status=400)

    order.place_order()
    order.save()
    return Response({"success": "your order is placed"})
