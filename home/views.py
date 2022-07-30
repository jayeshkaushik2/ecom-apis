from django.shortcuts import render
from rest_framework.decorators import api_view
from .models import Detail, Homepage, Homepage_Images
from .serializers import DetailSz, Homepage_ImagesSz, HomepageSz
from rest_framework.response import Response
from rest_framework import viewsets


@api_view(["GET", "POST"])
def ecom_details(request):
    if request.method == "GET":
        details, created = Detail.objects.get_or_create()
        sz = DetailSz(details)
        return Response(sz.data)
    else:
        details, created = Detail.objects.get_or_create()
        sz = DetailSz(instance=details, data=request.data, partial=True)
        if sz.is_valid(raise_exception=True):
            sz.save()
            return Response(sz.data)


class homepage_ImageApi(viewsets.ModelViewSet):
    serializer_class = Homepage_ImagesSz

    def get_queryset(self):
        return Homepage_Images.objects.all()

@api_view(["GET", "POST"])
def homepage(request):
    if request.method == "GET":
        details, created = Homepage.objects.get_or_create()
        sz = HomepageSz(details)
        return Response(sz.data)
    else:
        details, created = Homepage.objects.get_or_create()
        sz = HomepageSz(instance=details, data=request.data, partial=True)
        if sz.is_valid(raise_exception=True):
            sz.save()
            return Response(sz.data)
