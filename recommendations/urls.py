from .views import PlaceView, SinglePlaceView, ProtectedPlacesView, ProtectedSinglePlaceView
from django.urls import path

urlpatterns = [
    path("places", PlaceView.as_view()),
    path("places/<int:pk>", SinglePlaceView.as_view()),
    path("auth/places", ProtectedPlacesView.as_view()),
    path("auth/places/<int:pk>", ProtectedSinglePlaceView.as_view()),

]
