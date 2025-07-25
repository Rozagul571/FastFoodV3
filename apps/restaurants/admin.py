from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin
from .models import Category, Restaurant

MPTT_ADMIN_LEVEL_INDENT = 20

@admin.register(Category)
class CategoryAdmin(DraggableMPTTAdmin):
    list_display = (
        'tree_actions',
        'indented_title',
        'name',
        'parent',
        'level',
    )
    list_display_links = (
        'indented_title',
    )
    list_filter = ('parent',)
    search_fields = ['name']

@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name', 'location')
    list_filter = ('name',)
    search_fields = ['name']

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.prefetch_related('promotions')