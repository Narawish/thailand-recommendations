from rest_framework import serializers
from .models import Place, Rating
from django.contrib.auth.models import User

# class CommentSerializers(serializers.ModelSerializer):
#     user = serializers.StringRelatedField()

#     class Meta:
#         model = Comment
#         fields = ["id","user","content","created_at"]

class RatingSerializers(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ["id", "score", "user", "content"]

class PlaceSerializers(serializers.ModelSerializer):
    average_rating = serializers.FloatField(read_only=True)
    comments = RatingSerializers(many=True, read_only=True)
    rating_count = serializers.SerializerMethodField()
    class Meta:
        model = Place
        fields = ["id","name","province","latitude","longitude","average_rating","rating_count","comments"]

    def get_rating_count(self, obj):
        return obj.ratings.count()

class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id","username","email"]

class RecommendationSerializer(serializers.Serializer):
    min_distance = serializers.FloatField()
    sorted_places = serializers.ListField()
    
