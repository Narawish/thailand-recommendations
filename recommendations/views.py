from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from .models import Place
from .serializers import PlaceSerializers
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.db.models import Avg, Count

# Create your views here.

class PlaceListCreateView(ListCreateAPIView):
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

