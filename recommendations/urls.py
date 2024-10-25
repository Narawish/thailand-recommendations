from .views import (
    PlaceListCreateView, 
    ProtectedPlaceListCreateView, 
    DetailedView,
    ProtectedRatingView
)
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    path("places/", PlaceListCreateView.as_view(), name="places-list"),
    path("admin/places/", ProtectedPlaceListCreateView.as_view(), name="auth-places-list"),
    path('token/', TokenObtainPairView.as_view(), name="token-view"),
    path("places/<int:pk>/", DetailedView.as_view(), name="single-place-view"),
    path("places/<int:pk>/ratings", ProtectedRatingView.as_view(), name="place-rating"),
#     path("auth/places/<int:pk>", ProtectedSinglePlaceView.as_view()),

]
