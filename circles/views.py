# Django
from django.shortcuts import get_object_or_404
# Django REST Framework
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
# App
from circles.models import Circle, Membership
from circles.permissions import IsCircleAdmin
from circles.serializers import CircleSerializer, MembershipModelSerializer


# Circle views

@api_view(['GET'])
def list_circles(request):
    circles = Circle.objects.all()
    serializer = CircleSerializer(circles, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_circle(request, slug_name):
    circle = get_object_or_404(Circle, slug_name=slug_name)
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
def update_circle(request, slug_name):
    circle = get_object_or_404(Circle, slug_name=slug_name)
    serializer = CircleSerializer(instance=circle, data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated, IsCircleAdmin])
def delete_circle(request, slug_name):
    circle = get_object_or_404(Circle, slug_name=slug_name)
    circle.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


# Membership Views

@api_view(['GET'])
def get_circle_members(request, slug_name):
    circle = get_object_or_404(Circle, slug_name=slug_name)
    memberships = Membership.objects.filter(circle=circle, is_active=True)
    serializer = MembershipModelSerializer(memberships, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
