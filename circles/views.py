# Django
from django.shortcuts import get_object_or_404
# Django REST Framework
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
# App
from circles.models import Circle, Membership, Invitation
from circles.permissions import IsCircleAdmin, IsActiveCircleMember
from circles.serializers import CircleSerializer, MembershipSerializer
from users.models import User


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
                              is_admin=True)
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
@permission_classes([IsAuthenticated, IsActiveCircleMember])
def get_circle_members(request, slug_name):
    circle = get_object_or_404(Circle, slug_name=slug_name)
    memberships = Membership.objects.filter(circle=circle, is_active=True)
    serializer = MembershipSerializer(memberships, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsActiveCircleMember])
def get_circle_member(request, slug_name, username):
    circle = get_object_or_404(Circle, slug_name=slug_name)
    user = get_object_or_404(User, username=username)
    membership = get_object_or_404(Membership, user=user, circle=circle, is_active=True)
    serializer = MembershipSerializer(membership)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated, IsCircleAdmin])
def kick_circle_member(request, slug_name, username):
    circle = get_object_or_404(Circle, slug_name=slug_name)
    user = get_object_or_404(User, username=username)
    membership = get_object_or_404(Membership, user=user, circle=circle)
    membership.is_active = False
    membership.save()
    return Response(status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsActiveCircleMember])
def get_invitations(request, slug_name):
    circle = get_object_or_404(Circle, slug_name=slug_name)
    invited_members = Membership.objects.filter(circle=circle, invited_by=request.user, is_active=True)
    unused_invitations = Invitation.objects.filter(circle=circle,
                                                   issued_by=request.user, used=False).values_list('code', flat=True)
    data = {
        'unused_invitations': unused_invitations,
        'invited_members': MembershipSerializer(invited_members, many=True).data
    }
    return Response(data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsActiveCircleMember])
def create_invitation(request, slug_name):
    circle = get_object_or_404(Circle, slug_name=slug_name)
    invitation = Invitation.objects.create(issued_by=request.user, circle=circle)
    data = {f'Circle {circle.slug_name}': invitation.code}
    return Response(data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def join_circle(request, slug_name):
    circle = get_object_or_404(Circle, slug_name=slug_name)
    serializer = MembershipSerializer(data=request.data,
                                      context={'circle': circle, 'user': request.user, 'code': request.data})
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)
