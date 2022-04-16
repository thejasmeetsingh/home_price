import uuid

from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    email = models.EmailField(_("email address"), unique=True)
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


class HomePrice(models.Model):
    # Base Fields
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

    # CSV Fields
    date_time = models.DateTimeField()
    price = models.DecimalField(max_digits=15, decimal_places=2)
    bedrooms = models.FloatField()
    bathrooms = models.FloatField(default=0)
    sqft_living = models.PositiveIntegerField()
    sqft_lot = models.PositiveIntegerField()
    floors = models.FloatField()
    waterfront = models.PositiveIntegerField()
    view = models.PositiveIntegerField()
    condition = models.PositiveIntegerField()
    sqft_above = models.PositiveIntegerField()
    sqft_basement = models.PositiveIntegerField()
    yr_built = models.PositiveIntegerField()
    yr_renovated = models.PositiveIntegerField()
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    statezip = models.CharField(max_length=25)
    country = models.CharField(max_length=10)

    class Meta:
        ordering = ('-created_on',)
