# Django
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
# Utils
from utils.models import KRideModel


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
