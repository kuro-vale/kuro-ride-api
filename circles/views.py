# Django
from django.shortcuts import get_object_or_404
# Django REST Framework
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
# App Models
from circles.models import Circle, Membership
# App
from circles.permissions import IsCircleAdmin
from circles.serializers import CircleSerializer


@api_view(['GET'])
def list_circles(request):
    circles = Circle.objects.all()
    serializer = CircleSerializer(circles, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_circle(request, circle_id):
    circle = get_object_or_404(Circle, pk=circle_id)
    serializer = CircleSerializer(circle)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsCircleAdmin])
def create_circle(request):
    user = request.user
    profile = user.profile
    serializer = CircleSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    circle = serializer.save()
    Membership.objects.create(user=user, profile=profile, circle=circle,
                              is_admin=True, remaining_invitation=10)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['PUT'])
@permission_classes([IsAuthenticated, IsCircleAdmin])
def update_circle(request, circle_id):
    circle = get_object_or_404(Circle, pk=circle_id)
    serializer = CircleSerializer(instance=circle, data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated, IsCircleAdmin])
def delete_circle(request, circle_id):
    circle = get_object_or_404(Circle, pk=circle_id)
    circle.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
