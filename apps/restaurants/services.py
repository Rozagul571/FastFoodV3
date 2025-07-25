from apps.restaurants.models import Restaurant
from django.contrib.gis.geos import Point

def build_tree(queryset):
    categories = {}
    root = []
    for cat in queryset:
        cat_data = {'id': cat.id, 'name': cat.name, 'children': []}
        categories[cat.id] = cat_data
        if cat.parent_id is None:
            root.append(cat_data)
        elif cat.parent_id in categories:
            categories[cat.parent_id]['children'].append(cat_data)
    return root