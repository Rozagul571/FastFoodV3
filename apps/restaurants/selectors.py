from apps.restaurants.models import Restaurant

def get_restaurants():
    return Restaurant.objects.all()

def get_restaurants_category(category_id):
    return Restaurant.objects.filter(categories__id=category_id).distinct()