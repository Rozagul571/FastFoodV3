from django.contrib import admin
from .models import Dish

@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'category']
    list_filter = ['category']
    search_fields = ['name']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.prefetch_related('category__restaurant')

    def restaurant(self, obj):
        return obj.restaurant
    restaurant.short_description = 'Restaurant'