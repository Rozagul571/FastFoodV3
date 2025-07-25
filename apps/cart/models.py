from django.db import models

from apps.restaurants.models import Restaurant
from apps.users.models import User
from apps.dishes.models import Dish

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='carts')
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE, null=True, blank=True, related_name='carts')
    quantity = models.PositiveIntegerField(default=1)
    total_quantity = models.PositiveIntegerField(default=0)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, null=True, blank=True, related_name='carts')

    def __str__(self):
        return f"Cart for {self.user.phone_number} - {self.dish.name if self.dish else 'None'}"