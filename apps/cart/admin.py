from django.contrib import admin

from apps.cart.models import Cart


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    pass