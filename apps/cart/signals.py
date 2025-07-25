from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Cart
from .utils import update_cart_totals
from apps.restaurants.models import Restaurant

@receiver(post_save, sender=Cart)
def update_cart(sender, instance, created, **kwargs):
    update_fields = kwargs.get('update_fields')
    if update_fields is None or 'total_quantity' not in update_fields:
        if created is True or instance.dish is not None:
            update_cart_totals(instance)

@receiver(post_save, sender='users.User')
def create_cart_for_new_user(sender, instance, created, **kwargs):
    if created is True:
        default_restaurant = Restaurant.objects.first()
        if default_restaurant is not None:
            Cart.objects.get_or_create(
                user=instance,
                defaults={'dish': None, 'quantity': 0, 'total_quantity': 0})