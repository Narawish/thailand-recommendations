from django.urls import path
# from .views import CustomTokenPairView
from rest_framework_simplejwt.views import TokenObtainPairView



urlpatterns = [
    path('token/', TokenObtainPairView.as_view())
]
