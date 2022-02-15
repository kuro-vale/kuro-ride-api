# Django
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
# Utils
from utils.models import KRideModel


# User Models

class User(KRideModel, AbstractUser):
    email = models.EmailField('email address', unique=True,
                              error_messages={'unique': 'A user with that email already exist'})
    phone_regex = RegexValidator(regex=r'\+?1?\d{9,15}$', message='Invalid format')
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    is_client = models.BooleanField('client_status', default=True)
    is_verified = models.BooleanField('verified', default=False)

    def __str__(self):
        return self.username

    def get_short_name(self):
        return self.username


# Profile Models

class Profile(KRideModel):
    user = models.OneToOneField('users.User', on_delete=models.CASCADE)
    image = models.ImageField('profile picture', upload_to='users/static/users/images', blank=True, null=True)
    biography = models.TextField(max_length=500, blank=True)
    # Stats
    rides_taken = models.PositiveIntegerField(default=0)
    rides_offered = models.PositiveIntegerField(default=0)
    reputation = models.FloatField(default=3.0, help_text='users reputation based on the rides taken and offered')

    def __str__(self):
        return str(self.user)
