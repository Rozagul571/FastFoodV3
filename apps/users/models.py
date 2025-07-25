from django.contrib.auth.models import AbstractUser
from django.contrib.gis.db.models import PointField
from django.core.exceptions import ValidationError
from django.db import models

from apps.users.managers import UserManager


class User(AbstractUser):
    phone_number = models.CharField(max_length=15, unique=True, null=False)
    class Role(models.TextChoices):
        CUSTOMER = 'customer', 'Customer'
        COURIER = 'courier', 'Courier'
        RESTAURANTOWNER = 'restaurantOwner', 'RestaurantOwner'
        RESTAURANTMANAGER = 'restaurantManager', 'RestaurantManager'
        ADMIN = 'admin', 'Administrator'
        OSHPAZ = 'oshpaz', 'Oshpaz'
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []
    username = None
    objects = UserManager()
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.CUSTOMER)

    def save(self, *args, **kwargs):
        if self.pk:
            orig = User.objects.get(pk=self.pk)
            if orig.phone_number != self.phone_number:
                raise ValidationError("Phone number cannot be changed.")
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.phone_number)

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')
    address = models.CharField(max_length=255)
    entrance = models.CharField(max_length=50, blank=True, null=True)
    floor = models.IntegerField(blank=True, null=True)
    apartment = models.CharField(max_length=50, blank=True, null=True)
    location = PointField(srid=4326)

    def __str__(self):
        return str(self.address)