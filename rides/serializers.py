# Python
from datetime import timedelta
# Django
from django.db.models import Avg
from django.utils import timezone
# Django REST Framework
from rest_framework import serializers
# APP
from circles.models import Membership
from rides.models import Ride, Rating
from users.serializers import UserModelSerializer


class RideModelSerializer(serializers.ModelSerializer):
    offered_by = serializers.CharField()
    passengers = UserModelSerializer(read_only=True, many=True)

    class Meta:
        model = Ride
        exclude = ('offered_in', 'created', 'modified')
        read_only_fields = ('offered_in', 'offered_by', 'rating')

    def update(self, instance, validated_data):
        now = timezone.now()
        if instance.departure_date <= now:
            raise serializers.ValidationError('Ongoing rides cannot be modified')
        instance.available_seats = validated_data.get('available_seats', instance.available_seats)
        instance.comments = validated_data.get('comments', instance.comments)
        instance.departure_location = validated_data.get('departure_location', instance.departure_location)
        instance.departure_date = validated_data.get('departure_date', instance.departure_date)
        instance.arrival_location = validated_data.get('available_seats', instance.arrival_location)
        instance.arrival_date = validated_data.get('arrival_date', instance.arrival_date)
        instance.save()
        return instance


class CreateRideSerializer(serializers.ModelSerializer):
    available_seats = serializers.IntegerField(min_value=1, max_value=15)

    class Meta:
        model = Ride
        exclude = ('offered_in', 'passengers', 'rating', 'is_active', 'offered_by', 'created', 'modified')

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


class JoinRideSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ride
        fields = '__all__'

    def validate(self, attrs):
        ride = self.context['ride']
        if ride.offered_by == self.context['user']:
            raise serializers.ValidationError('You are the owner of this ride')
        if ride.departure_date <= timezone.now():
            raise serializers.ValidationError("You can't join this ride now")
        if ride.available_seats < 1:
            raise serializers.ValidationError('Ride is already full')
        if ride.passengers.filter(pk=self.context['user'].pk).exists():
            raise serializers.ValidationError('passenger is already in this trip')
        return attrs

    def update(self, instance, validated_data):
        ride = self.context['ride']
        user = self.context['user']
        ride.passengers.add(user)
        ride.available_seats -= 1
        ride.save()
        profile = user.profile
        profile.rides_taken += 1
        profile.save()
        membership = self.context['membership']
        membership.rides_taken += 1
        membership.save()
        circle = self.context['circle']
        circle.rides_taken += 1
        circle.save()
        return ride


class CreateRideRatingSerializer(serializers.ModelSerializer):
    rating = serializers.FloatField(min_value=0, max_value=5)
    comments = serializers.CharField(required=False)

    class Meta:
        model = Rating
        fields = ('rating', 'comments')

    def validate(self, attrs):
        user = self.context['user']
        ride = self.context['ride']
        if ride.offered_by == user:
            raise serializers.ValidationError('You are the owner of this ride')
        if not ride.passengers.filter(pk=user.pk).exists():
            raise serializers.ValidationError('User is not a passenger')
        rating = Rating.objects.filter(circle=self.context['circle'],
                                       ride=ride, rating_user=user)
        if rating.exists():
            raise serializers.ValidationError('Rating have already been emitted')
        return attrs

    def create(self, validated_data):
        circle = self.context['circle']
        ride = self.context['ride']
        rating_user = self.context['user']
        offered_by = self.context['ride'].offered_by
        Rating.objects.create(circle=circle, ride=ride, rating_user=rating_user,
                              rated_user=offered_by, **validated_data)
        ride_avg = round(Rating.objects.filter(circle=circle,
                                               ride=ride).aggregate(Avg('rating'))['rating__avg'], 1)
        ride.rating = ride_avg
        ride.save()
        user_av = round(Rating.objects.filter(rated_user=offered_by).aggregate(Avg('rating'))['rating__avg'], 1)
        offered_by.profile.reputation = user_av
        offered_by.profile.save()
        return ride
