from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, RetrieveAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Place, Rating
from django.db.utils import IntegrityError
import logging
from thailand_recommendations import settings
import jwt

from django.contrib.auth import get_user_model
from .serializers import PlaceSerializers, RatingSerializers, RecommendationSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser, IsAuthenticated
from django.db.models import Avg, Count
import numpy as np
from .utils import get_min_distance


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


class ProtectedRatingView(APIView):
    def get_user_from_token(self,request, token):
        try:
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=['HS256']
            )

            User = get_user_model()
            
            return User.objects.get(id=payload['user_id'])
        except (jwt.DecodeError, User.DoesNotExist):
            return None
    # Get all rating of a place
    def get(self, request, pk):
        # Get only certain place ratings and comments
        ratings = Rating.objects.filter(place_id=pk)
        if not ratings:
            return Response(
                {
                    "place_id":pk,
                    "average_rating": 0,
                    "data":[]
                }, status=status.HTTP_404_NOT_FOUND
            )
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

    # post new rating
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
        user = self.get_user_from_token(request,token)
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

        try:
            Rating.objects.create(
                place = place,
                user = user,
                score = score,
                content = content
            )
            return Response(
            {
                "message": "Rating created",
                "data": {
                    "place_id":place.id,
                    "user_id":user.id,
                    "score":score,
                    "content":content
                } 
            },
            status=status.HTTP_201_CREATED)
        except IntegrityError:
            return Response(
                {
                    "error": "Unable to create rating",
                    "message": "rating already exists",
                },
                status=status.HTTP_400_BAD_REQUEST
            )

    # put ratings
    def put(self, request, pk):
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
        user = self.get_user_from_token(request,token)

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
        
        rating = Rating.objects.filter(place_id=pk)
        if not rating:
            return Response(
                {
                    "error":f"no rating of place_id {place.id}"
                }
            )
        try:
            rating.update(
                place = place,
                user = user,
                score = score,
                content = content
            )

            return Response(
            {
                "message": "Rating updated",
                "data": {
                    "place_id":place.id,
                    "user_id":user.id,
                    "score":score,
                    "content":content
                } 
            },
            status=status.HTTP_201_CREATED
        )
        except:
            return Response(
                {
                    "error": "Unable to update rating",
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
    def delete(self, request, pk):
        # Get token from headers
        auth_header = request.headers.get("Authorization","").split()

        if len(auth_header) != 2 or auth_header[0].lower() != 'bearer':
            return Response(
                {
                    "error":"Invalid authorization header"
                },
                status= status.HTTP_401_UNAUTHORIZED
            )
        token = auth_header[1]
        user = self.get_user_from_token(request,token)

        if not user:
            return Response(
                {
                    "error":"Invalid token"
                },
                status= status.HTTP_401_UNAUTHORIZED
            )
        place = get_object_or_404(Place, pk=pk)
        try:
            Rating.objects.filter(place_id=pk, user_id=user.id).delete()
            return Response({
                "message":"delete successfully"
            })
        except:
            return Response(
                {
                    "error":"Unable to delete rating"
                }
            )
        
class RecommendationView(ListAPIView):
    def get(self, request):
        objects = Place.objects.annotate(
            avg_rating=Avg("ratings__score"),
            total_rating=Count("ratings")
        )
        random_number = np.random.randint(0,len(objects)-5)
        places = objects[random_number:random_number+5]
        # print(places)
        min_distance, sorted_places = get_min_distance(places)

        serializer = RecommendationSerializer({"min_distance":min_distance, 
                                                    "sorted_places":sorted_places})
        
        return Response(serializer.data, status=status.HTTP_200_OK)
