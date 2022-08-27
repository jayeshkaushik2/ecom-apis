from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import viewsets
from .models import Order, DeliveryLocation
from .serializers import OrderSz, DeliveryLocationSz

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
def orderApi(request):
    if request.method == "GET":
        return Response({'data':["data","data"]})
    else:
        return Response({"success":"post"})