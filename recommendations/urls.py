from .views import PlaceListCreateView, ProtectedPlaceListCreateView
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    path("places/", PlaceListCreateView.as_view(), name="places-list"),
    path("admin/places/", ProtectedPlaceListCreateView.as_view(), name="auth-places-list"),
    path('token/', TokenObtainPairView.as_view()),
#     path("auth/places", ProtectedPlacesView.as_view()),
#     path("auth/places/<int:pk>", ProtectedSinglePlaceView.as_view()),

]
