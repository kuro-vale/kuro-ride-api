# Python
from datetime import timedelta
# Django
from django.utils import timezone
# Django REST Framework
from rest_framework import serializers
# APP
from circles.models import Membership
from rides.models import Ride


class CreateRideSerializer(serializers.ModelSerializer):
    available_seats = serializers.IntegerField(min_value=1, max_value=15)

    class Meta:
        model = Ride
        exclude = ('offered_in', 'passengers', 'rating', 'is_active', 'offered_by', 'id')

    def validate(self, attrs):
        # Validate departure date
        min_date = timezone.now() + timedelta(minutes=10)
        if attrs.get('departure_date') < min_date:
            raise serializers.ValidationError('Departure time must be at least pass the next 20 minutes window')
        # Validate attrs
        user = self.context['offered_by']
        circle = self.context['circle']
        membership = Membership.objects.get(user=user, circle=circle, is_active=True)
        self.context['membership'] = membership
        # Validate arrival date
        if attrs.get('arrival_date') <= attrs.get('departure_date'):
            raise serializers.ValidationError('Departure must happen after arrival date')
        return attrs

    def create(self, validated_data):
        circle = self.context['circle']
        ride = Ride.objects.create(**validated_data, offered_in=circle, offered_by=self.context['offered_by'])
        circle.rides_offered += 1
        circle.save()
        membership = self.context['membership']
        membership.rides_offered += 1
        membership.save()
        profile = self.context['offered_by'].profile
        profile.rides_offered += 1
        profile.save()
        return ride
