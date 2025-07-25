from django.contrib import admin

from apps.orders.models import Order
from apps.users.models import User, Address


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    pass