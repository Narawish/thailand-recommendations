from .views import PlaceView, SinglePlaceView
from django.urls import path

urlpatterns = [
    path("places", PlaceView.as_view()),
    path("places/<int:pk>", SinglePlaceView.as_view())
]
