# Django REST Framework
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
# Serializer
from users.serializers import UserLoginSerializer, UserModelSerializer, UserSignUpSerializer, \
    AccountVerificationSerializer


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
