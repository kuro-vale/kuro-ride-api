# Django
from django.contrib.auth import authenticate, password_validation
from django.core.validators import RegexValidator
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
        authenticate(username=user.email, password=user.password)
        return user


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(min_length=8)

    def validate(self, data):
        user = authenticate(username=data['email'], password=data['password'])
        if not user:
            raise serializers.ValidationError('Invalid credentials')
        self.context['user'] = user
        return data

    def create(self, validated_data):
        token, created = Token.objects.get_or_create(user=self.context['user'])
        return self.context['user'], token.key
