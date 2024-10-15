from django.db import models
from django.core.validators import MinValueValidator

# Create your models here.
class Place(models.Model):
    name = models.CharField(max_length=200)
    province = models.CharField(max_length=100)
    latitude = models.FloatField(validators=[MinValueValidator(0)])
    longitude = models.FloatField(validators=[MinValueValidator(0)])

    # Ordering the class with 'name' field
    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
