from .views import (
    PlaceListCreateView, 
    ProtectedPlaceListCreateView, 
    DetailedView,
    ProtectedRatingView,
    RecommendationView
)
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("places/", PlaceListCreateView.as_view(), name="places-list"),
    path("admin/places/", ProtectedPlaceListCreateView.as_view(), name="auth-places-list"),
    path("places/<int:pk>/", DetailedView.as_view(), name="single-place-view"),
    path("places/<int:pk>/ratings", ProtectedRatingView.as_view(), name="place-rating"),
    path("places/recommend", RecommendationView.as_view(), name="place-recommend")
#     path("auth/places/<int:pk>", ProtectedSinglePlaceView.as_view()),

]
