import django_filters
from .models import Dish

class DishFilter(django_filters.FilterSet):
    price_min = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    price_max = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    ordering = django_filters.OrderingFilter(
        fields=(('price', 'price'), ('name', 'name')),
        field_labels={'price': 'Price', 'name': 'Name'}
    )
    search = django_filters.CharFilter(method='filter_search')
    promotion = django_filters.ChoiceFilter(choices=Dish._meta.get_field('promotion').choices, field_name='promotion')

    class Meta:
        model = Dish
        fields = ['price_min', 'price_max', 'ordering', 'search', 'promotion']

    def filter_search(self, queryset, name, value):
        if value:
            return queryset.filter(name__icontains=value)
        return queryset