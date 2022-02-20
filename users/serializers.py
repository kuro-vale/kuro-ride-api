# Python
from datetime import timedelta
# PyJWT
import jwt
# Django
from django.conf import settings
from django.contrib.auth import authenticate, password_validation
from django.core.mail import send_mail
from django.core.validators import RegexValidator
from django.utils import timezone
# Django REST Framework
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.validators import UniqueValidator
# Models
from users.models import User, Profile


class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'phone_number'
        )


class UserSignUpSerializer(serializers.Serializer):
    email = serializers.EmailField(validators=[UniqueValidator(queryset=User.objects.all())])
    username = serializers.CharField(min_length=2, max_length=20,
                                     validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(min_length=8)
    phone_regex = RegexValidator(regex=r'\+?1?\d{9,15}$', message='Invalid format')
    phone_number = serializers.CharField(validators=[phone_regex], required=False)
    first_name = serializers.CharField(min_length=2, required=False)
    last_name = serializers.CharField(min_length=2, required=False)

    def validate(self, data):
        passwd = data['password']
        password_validation.validate_password(passwd)
        return data

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        Profile.objects.create(user=user)
        self.send_verification_email(user)
        return user

    def send_verification_email(self, user):
        verification_token = self.gen_verification_token(user)
        send_mail(
            f'Welcome to KuroRide {user}',
            f'Your verification token is: {verification_token}',
            'noreply@kuroride.com',
            [user.email],
        )

    @staticmethod
    def gen_verification_token(user):
        exp_date = timezone.now() + timedelta(hours=1)
        payload = {
            'user': user.username,
            'exp': int(exp_date.timestamp()),
            'type': 'email_confirmation'
        }
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
        return token

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.username = validated_data.get('username', instance.username)
        instance.password = validated_data.get('password', instance.password)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.save()
        return instance


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(min_length=8)

    def validate(self, data):
        user = authenticate(username=data['email'], password=data['password'])
        if not user:
            raise serializers.ValidationError('Invalid credentials')
        if not user.is_verified:
            raise serializers.ValidationError('Account is not active yet')
        self.context['user'] = user
        return data

    def create(self, validated_data):
        token, created = Token.objects.get_or_create(user=self.context['user'])
        return self.context['user'], token.key


class AccountVerificationSerializer(serializers.Serializer):
    token = serializers.CharField()

    def validate(self, data):
        try:
            payload = jwt.decode(data.get('token'), settings.SECRET_KEY, algorithms='HS256')
        except jwt.ExpiredSignatureError:
            raise serializers.ValidationError('Verification link has expired')
        except jwt.PyJWTError:
            raise serializers.ValidationError('Invalid Token')
        if payload['type'] != 'email_confirmation':
            raise serializers.ValidationError('Invalid Token')
        self.context['payload'] = payload
        return data

    def save(self):
        payload = self.context['payload']
        user = User.objects.get(username=payload['user'])
        user.is_verified = True
        user.save()
