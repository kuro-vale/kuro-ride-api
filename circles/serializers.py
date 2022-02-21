# Django
from django.utils import timezone
# Django REST Framework
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
# App
from circles.models import Circle, Membership, Invitation
from users.serializers import UserModelSerializer


class CircleSerializer(serializers.Serializer):
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


class MembershipSerializer(serializers.Serializer):
    user = UserModelSerializer(read_only=True)
    invited_by = serializers.StringRelatedField(read_only=True)
    joined_at = serializers.DateTimeField(source='created', read_only=True)

    class Meta:
        model = Membership
        fields = ('user', 'is_admin', 'is_active',
                  'invited_by', 'rides_taken', 'rides_offered',
                  'joined_at')
        read_only_fields = ('rides_taken', 'rides_offered')

    def validate(self, attrs):
        circle = self.context['circle']
        user = self.context['user']
        membership = Membership.objects.filter(circle=circle, user=user, is_active=True)
        code = self.context['code'].get('code')
        if membership:
            raise serializers.ValidationError('User is already member of this circle')
        try:
            invitation = Invitation.objects.get(code=code, circle=circle, used=False)
        except Invitation.DoesNotExist:
            raise serializers.ValidationError('Invalid invitation code')
        if circle.is_limited and circle.members.count() >= circle.members_limit:
            raise serializers.ValidationError('Circle has reached its member limit')
        self.context['invitation'] = invitation
        return attrs

    def create(self, validated_data):
        circle = self.context['circle']
        user = self.context['user']
        invitation = self.context['invitation']
        now = timezone.now()
        rejoin = Membership.objects.get(circle=circle, user=user, is_active=False)
        invitation.used_by = user
        invitation.used = True
        invitation.used_at = now
        invitation.save()
        if rejoin:
            rejoin.is_active = True
            rejoin.save()
            return rejoin
        membership = Membership.objects.create(user=user,
                                               profile=user.profile,
                                               circle=circle,
                                               invited_by=invitation.issued_by)
        return membership
