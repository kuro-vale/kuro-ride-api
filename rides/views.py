# Django
from django.shortcuts import get_object_or_404
# Django REST Framework
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
# App
from circles.models import Circle
from circles.permissions import IsActiveCircleMember
from rides.serializers import CreateRideSerializer


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsActiveCircleMember])
def create_ride(request, slug_name):
    circle = get_object_or_404(Circle, slug_name=slug_name)
    serializer = CreateRideSerializer(data=request.data, context={'circle': circle, 'offered_by': request.user})
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)
