from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.
# Generate Place model
class Place(models.Model):
    name = models.CharField(max_length=200)
    province = models.CharField(max_length=100)
    latitude = models.FloatField(validators=[MinValueValidator(0)])
    longitude = models.FloatField(validators=[MinValueValidator(0)])
    # created_at = models.DateTimeField(default=datetime.now, null=False)
    # updated_at = models.DateTimeField(default=datetime.now, null=False)

    class Meta:
        ordering = ["name"]
        
    def __str__(self):
        return self.name
    
    # Getting average rating of each place
    @property
    def average_rating(self):
        ratings = self.ratings.all()
        if ratings:
            return round(sum(rating.score for rating in ratings) / len(ratings),2)
        return 0

# Generate Rating model
class Rating(models.Model):
    place = models.ForeignKey(Place, related_name="ratings", on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="ratings", on_delete=models.CASCADE)
    score = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['place','user']

# Generate Comment model
class Comment(models.Model):
    place = models.ForeignKey(Place, related_name="comments", on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="comments", on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now=True)
    
