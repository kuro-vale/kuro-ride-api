# Django REST Framework
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
# Models
from circles.models import Circle


class CircleSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    name = serializers.CharField(max_length=140)
    slug_name = serializers.SlugField(validators=[UniqueValidator(queryset=Circle.objects.all())], max_length=40)
    about = serializers.CharField(max_length=255, required=False)
    rides_taken = serializers.IntegerField(default=0, required=False, read_only=True)
    rides_offered = serializers.IntegerField(default=0, required=False, read_only=True)
    members_limit = serializers.IntegerField(default=0, required=False)
    is_limited = serializers.BooleanField(default=False)
    is_public = serializers.BooleanField(read_only=True, default=True)
    verified = serializers.BooleanField(read_only=True, default=False)

    def validate(self, attrs):
        members_limit = attrs.get('members_limit', 0)
        is_limited = attrs.get('is_limited', False)
        if is_limited ^ bool(members_limit):
            raise serializers.ValidationError('If circle is limited, a member limit must be provided')
        return attrs

    def create(self, validated_data):
        return Circle.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.slug_name = validated_data.get('slug_name', instance.slug_name)
        instance.about = validated_data.get('about', instance.about)
        instance.rides_taken = validated_data.get('rides_taken', instance.rides_taken)
        instance.rides_offered = validated_data.get('rides_offered', instance.rides_offered)
        instance.members_limit = validated_data.get('members_limit', instance.members_limit)
        instance.is_limited = validated_data.get('is_limited', instance.is_limited)
        instance.is_public = validated_data.get('is_public', instance.is_public)
        instance.save()
        return instance
