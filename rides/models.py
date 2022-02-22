# Django
from django.db import models
# App
from circles.models import Circle
from users.models import User
from utils.models import KRideModel


class Ride(KRideModel):
    offered_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    offered_in = models.ForeignKey(Circle, on_delete=models.SET_NULL, null=True)
    passengers = models.ManyToManyField(User, related_name='passengers')
    available_seats = models.PositiveIntegerField(default=1)
    comments = models.TextField(blank=True)
    departure_location = models.CharField(max_length=255)
    departure_date = models.DateTimeField()
    arrival_location = models.CharField(max_length=255)
    arrival_date = models.DateTimeField()
    rating = models.FloatField(null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.departure_location} to {self.arrival_location} | {self.departure_date} - {self.arrival_date}'


class Rating(KRideModel):
    ride = models.ForeignKey(Ride, on_delete=models.CASCADE, related_name='rated_ride')
    circle = models.ForeignKey(Circle, on_delete=models.CASCADE)
    rating_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='rating_user')
    rated_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='rated_user')
    comments = models.TextField(blank=True)
    rating = models.FloatField(default=3.0)

    def __str__(self):
        return f'Ride: {self.ride.id} Rating: {self.rating}'
