# Django
from django.shortcuts import get_object_or_404
# Django REST Framework
from rest_framework.permissions import BasePermission
# App
from rides.models import Ride


class IsRideOwner(BasePermission):
    def has_permission(self, request, view):
        ride = get_object_or_404(Ride, pk=view.kwargs['ride_id'])
        return request.user == ride.offered_by
