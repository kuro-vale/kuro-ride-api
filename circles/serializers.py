# Django REST Framework
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
# Models
from circles.models import Circle


class CircleSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=140)
    slug_name = serializers.SlugField(validators=[UniqueValidator(queryset=Circle.objects.all())], max_length=40)
    about = serializers.CharField(max_length=255, required=False)
    rides_taken = serializers.IntegerField(default=0, required=False)
    rides_offered = serializers.IntegerField(default=0, required=False)
    members_limit = serializers.IntegerField(default=0, required=False)

    def create(self, validated_data):
        return Circle.objects.create(**validated_data)
