from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from .models import Place
from .serializers import PlaceSerializers
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser, IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.db.models import Avg, Count
import numpy as np

# Create your views here.

class PlaceListCreateView(ListAPIView):
    queryset = Place.objects.annotate(
        avg_rating=Avg("ratings__score"),
        total_rating=Count("ratings")
    )
    random_number = np.random.randint(0,len(queryset)-5)
    queryset = queryset[random_number:random_number+5]

    serializer_class = PlaceSerializers

    # Only Admin can add places
    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAdminUser()]
        return [IsAuthenticatedOrReadOnly()]

class ProtectedPlaceListCreateView(ListCreateAPIView):

    permission_classes = [IsAuthenticated()]
    queryset = Place.objects.annotate(
        avg_rating=Avg("ratings__score"),
        total_rating=Count("ratings")
    )
    serializer_class = PlaceSerializers

    # Only Admin can add places
    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAdminUser()]
        return [IsAuthenticatedOrReadOnly()]
class DetailedView(RetrieveUpdateDestroyAPIView):
    queryset = Place.objects.annotate(
        avg_rating=Avg("ratings__score"),
        total_rating=Count("ratings")
    )

    serializer_class = PlaceSerializers

     # Only Admin can put, patch, delete places
    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAdminUser()]
        return [IsAuthenticatedOrReadOnly()]

