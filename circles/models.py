# Django
from django.db import models
# Utils
from users.models import User, Profile
from utils.models import KRideModel


class Circle(KRideModel):
    """A circle is a private/public group where rides are offered and taken by users"""
    name = models.CharField('circle name', max_length=140)
    slug_name = models.SlugField(unique=True, max_length=40)
    about = models.CharField('circle description', max_length=255)
    members = models.ManyToManyField(User, through='Membership', through_fields=('circle', 'user'))
    picture = models.ImageField(upload_to='users/static/circles/images', blank=True, null=True)
    rides_offered = models.PositiveIntegerField(default=0)
    rides_taken = models.PositiveIntegerField(default=0)
    verified = models.BooleanField(default=False)
    is_public = models.BooleanField(default=True)

    is_limited = models.BooleanField(default=False, help_text='limited circles can grow up to a fixed numbers of users')
    members_limit = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta(KRideModel.Meta):
        ordering = ['-rides_taken', '-rides_offered']


class Membership(KRideModel):
    """ Membership is the table that hold the relationship between a user and a circle"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    circle = models.ForeignKey(Circle, on_delete=models.CASCADE)
    is_admin = models.BooleanField('circle admin', default=False)
    user_invitation = models.PositiveIntegerField(default=0)
    remaining_invitation = models.PositiveIntegerField(default=0)
    invited_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='invited_by')
    rides_taken = models.PositiveIntegerField(default=0)
    rides_offered = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField('status', default=True)

    def __str__(self):
        return f'@{self.user.username} at #{self.circle.slug_name}'
