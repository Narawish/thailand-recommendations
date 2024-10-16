from .views import PlaceListCreateView
from django.urls import path

urlpatterns = [
    path("places/", PlaceListCreateView.as_view(), name="places-list"),
#     path("places/<int:pk>", SinglePlaceView.as_view()),
#     path("auth/places", ProtectedPlacesView.as_view()),
#     path("auth/places/<int:pk>", ProtectedSinglePlaceView.as_view()),

]
