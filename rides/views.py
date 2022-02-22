# Python
from datetime import timedelta
# Django
from django.shortcuts import get_object_or_404
from django.utils import timezone
# Django REST Framework
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
# App
from circles.models import Circle, Membership
from circles.permissions import IsActiveCircleMember
from rides.models import Ride
from rides.permissions import IsRideOwner
from rides.serializers import CreateRideSerializer, RideModelSerializer, JoinRideSerializer


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsActiveCircleMember])
def create_ride(request, slug_name):
    circle = get_object_or_404(Circle, slug_name=slug_name)
    serializer = CreateRideSerializer(data=request.data, context={'circle': circle, 'offered_by': request.user})
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsActiveCircleMember])
def get_rides(request, slug_name):
    circle = get_object_or_404(Circle, slug_name=slug_name)
    offset = timezone.now() + timedelta(minutes=10)
    rides = Ride.objects.filter(offered_in=circle, departure_date__gte=offset, is_active=True)
    serializer = RideModelSerializer(rides, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated, IsRideOwner])
def update_ride(request, ride_id):
    ride = get_object_or_404(Ride, pk=ride_id)
    partial = request.method == 'PATCH'
    serializer = RideModelSerializer(ride, data=request.data, partial=partial)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsActiveCircleMember])
def join_ride(request, slug_name, ride_id):
    circle = get_object_or_404(Circle, slug_name=slug_name)
    membership = get_object_or_404(Membership, circle=circle, user=request.user)
    ride = get_object_or_404(Ride, pk=ride_id)
    serializer = JoinRideSerializer(ride, data=request.data,
                                    context={'ride': ride, 'user': request.user, 'circle': circle, 'membership': membership},
                                    partial=True)
    serializer.is_valid(raise_exception=True)
    ride = serializer.save()
    data = RideModelSerializer(ride).data
    return Response(data, status=status.HTTP_200_OK)
