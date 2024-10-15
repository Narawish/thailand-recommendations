from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from .models import Place
from .serializers import PlaceSerializers
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

# Create your views here.

# Get 5 Places
class PlaceView(ListAPIView):
    queryset = Place.objects.all()[:5]
    serializer_class = PlaceSerializers

# Get Single Place
class SinglePlaceView(RetrieveAPIView):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializers

# Get or Update All places
class ProtectedPlacesView(ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Place.objects.all()
    serializer_class = PlaceSerializers

class ProtectedSinglePlaceView(RetrieveUpdateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Place.objects.all()
    serializer_class = PlaceSerializers