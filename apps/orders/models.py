from django.db import models
from apps.users.models import User, Address
from apps.dishes.models import Dish

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')
    restaurant = models.ForeignKey('restaurants.Restaurant', on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')
    status = models.CharField(max_length=50, choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('sent', 'Sent'), ('cancelled', 'Cancelled')], default='pending')
    dishes = models.ManyToManyField(Dish, through='OrderItem', related_name='orders')

    def __str__(self):
        return f"Order {self.id} by {self.user.phone_number}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    class Meta:
        unique_together = ('order', 'dish')

    def __str__(self):
        return f"{self.quantity} x {self.dish.name}"