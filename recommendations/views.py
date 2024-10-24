from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, RetrieveAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Place, Rating
from django.contrib.auth import get_user_model

from .serializers import PlaceSerializers, RatingSerializers
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser, IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.db.models import Avg, Count
import numpy as np
import jwt
from thailand_recommendations import settings

# Create your views here.

class PlaceListCreateView(ListAPIView):
    queryset = Place.objects.annotate(
        avg_rating=Avg("ratings__score"),
        total_rating=Count("ratings")
    )
    random_number = np.random.randint(0,len(queryset)-5)
    queryset = queryset[random_number:random_number+5]

    serializer_class = PlaceSerializers

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

class RatingCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get_user_from_token(self, token):
        try:
            paylod = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=['HS256']
            )
            User = get_user_model()
            return User.objects.get(id=paylod['user_id'])
        except (jwt.DecodeError, ):
            return None

    def post(self, request, pk):

        #Get token from headers
        auth_header = request.headers.get("Authorization","").split()

        if len(auth_header) != 2 or auth_header[0].lower() != 'bearer':
            return Response(
                {
                    "error":"Invalid authorization header"
                },
                status= status.HTTP_401_UNAUTHORIZED
            )
        token = auth_header[1]
        user = self.get_user_from_token(token)
        if not user:
            return Response(
                {
                    "error":"Invalid token"
                },
                status= status.HTTP_401_UNAUTHORIZED
            )
        place = get_object_or_404(Place, pk=pk)
        score = request.data.get("score")
        content = request.data.get("content")
        
        if not 1 <= score <= 5:
            return Response(
                {
                    "error","score must be between 1 and 5"
                },
                status= status.HTTP_400_BAD_REQUEST
            )
        
        rating, created = Rating.objects.update_or_create(
            place = place,
            user = user,
            score = score,
            content = content
        )

        return Response(
            {
                "message": "Rating created" if created else "Rating updated",
                "data": {
                    "place_id":place.id,
                    "user_id":user.id,
                    "score":score,
                    "content":content
                } 
            },
            status=status.HTTP_201_CREATED
        )
    
    def get(self, request, pk):

        # Get only certain place ratings and comments
        ratings = Rating.objects.filter(place_id=pk)
        avg_ratings = sum(rating.score for rating in ratings) / len(ratings)
        return Response(
            {
                "place_id":pk,
                "average_rating": avg_ratings,
                "data":[{
                    "score":rating.score,
                    "user":rating.user.id,
                    "content":rating.content
                } for rating in ratings]
            }, 
            status=status.HTTP_200_OK
            )

