# Django
from django.shortcuts import get_object_or_404
# Django REST Framework
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
# App
from circles.models import Circle
from circles.serializers import CircleSerializer
from users.models import User
from users.serializers import UserLoginSerializer, UserModelSerializer, UserSignUpSerializer, \
    AccountVerificationSerializer, ProfileSerializer


class UserLoginAPIView(APIView):
    @staticmethod
    def post(request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, token = serializer.save()
        data = {
            'user': UserModelSerializer(user).data,
            'access_token': token
        }
        return Response(data, status=status.HTTP_200_OK)


class SignUpAPIView(APIView):
    @staticmethod
    def post(request):
        serializer = UserSignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = UserModelSerializer(user).data,
        return Response(data, status=status.HTTP_201_CREATED)


class AccountVerificationAPIView(APIView):
    @staticmethod
    def post(request):
        serializer = AccountVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {'message': 'Your account is verified'}
        return Response(data, status=status.HTTP_200_OK)


@api_view(['GET'])
def logout(request):
    request.user.auth_token.delete()
    return Response(status=status.HTTP_200_OK)


@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_user(request):
    partial = request.method == 'PATCH'
    serializer = UserSignUpSerializer(instance=request.user, data=request.data, partial=partial)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_user(request):
    request.user.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def get_user(request, username):
    user = get_object_or_404(User, username=username)
    circles = Circle.objects.filter(members=user)
    profile = user.profile
    serializer = UserModelSerializer(user)
    data = {
        'user': serializer.data,
        'profile': ProfileSerializer(profile).data,
        'circles': CircleSerializer(circles, many=True).data
    }
    return Response(data, status=status.HTTP_200_OK)


@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_profile(request):
    profile = request.user.profile
    partial = request.method == 'PATCH'
    serializer = ProfileSerializer(profile, data=request.data, partial=partial)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_200_OK)

