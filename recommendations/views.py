from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView
from .models import Place
from .serializers import PlaceSerializers

# Create your views here.

class PlaceView(ListCreateAPIView):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializers

class SinglePlaceView(RetrieveUpdateAPIView):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializers