# Django
from django.db import models
# Utils
from utils.models import KRideModel


class Circle(KRideModel):
    """A circle is a private/public group where rides are offered and taken by users"""
    name = models.CharField('circle name', max_length=140)
    slug_name = models.SlugField(unique=True, max_length=40)
    about = models.CharField('circle description', max_length=255)
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
