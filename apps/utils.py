from math import sin, cos, atan2, sqrt, radians
from decimal import Decimal
from django.db.models import Sum
from apps.cart.models import Cart
from apps.cart.utils import update_cart_totals
from apps.orders.models import OrderItem

def calculate_distance(user_location, rest_location):
    if user_location is None or rest_location is None:
        return 0
    lat1 = radians(user_location.y)
    lon1 = radians(user_location.x)
    lat2 = radians(rest_location.y)
    lon2 = radians(rest_location.x)
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = 6371 * c
    return round(distance, 3)

def calculate_delivery_time(order):
    order_items = order.items.all()
    if not order_items.exists():
        return {
            'delivery_time': 0,
            'delivery_price': Decimal('0.00'),
            'total_price': Decimal('0.00')
        }

    result = order_items.aggregate(total_quantity=Sum('quantity'))
    quantity = result['total_quantity'] or 0
    preparation = (quantity * 75) // 60
    user_address = order.address
    restaurant = order.restaurant
    if user_address and user_address.location and restaurant and restaurant.location:
        distance_km = calculate_distance(user_address.location, restaurant.location)
    else:
        distance_km = 0
    delivery = max(5, int(distance_km * 3))
    total_time = preparation + delivery

    delivery_price = Decimal(str(distance_km * 1000)).quantize(Decimal('0.00'))
    delivery_price = max(delivery_price, Decimal('5000.00'))  #  5000 so'm km un


    total_price = sum(item.price for item in order_items) + delivery_price

    return {
        'delivery_time': int(total_time),
        'delivery_price': delivery_price,
        'total_price': total_price
    }

def calculate_order_totals(user_or_cart):
    if hasattr(user_or_cart, 'user'):
        user = user_or_cart.user
    else:
        user = user_or_cart

    carts = Cart.objects.filter(user=user)

    if not carts.exists():
        return {
            'total_quantity': 0,
            'delivery_fee': Decimal('0.00'),
            'total_price': Decimal('0.00'),
            'delivery_time': 0,
            'items': []
        }

    total_quantity = 0
    total_price = Decimal('0.00')
    items = []

    for cart in carts:
        if cart.dish is None:
            continue
        totals = update_cart_totals(cart)
        total_quantity += totals['total_quantity']
        total_price += totals['price']
        if cart.dish.promotion:
            promotion_quantity = cart.dish.adjusted_quantity * cart.quantity
        else:
            promotion_quantity = cart.quantity

        if cart.dish.category and cart.dish.category.restaurant:
            restaurant_id = cart.dish.category.restaurant.id
            restaurant_name = cart.dish.category.restaurant.name
        else:
            restaurant_id = None
            restaurant_name = None

        items.append({
            'dish': cart.dish.id,
            'quantity': cart.quantity,
            'total_quantity': totals['total_quantity'],
            'promotion_quantity': promotion_quantity,
            'price': float(totals['price']),
            'promotion': cart.dish.promotion.name if cart.dish.promotion else None,
            'restaurant_id': restaurant_id
        })

    first_cart = carts.first()
    if first_cart and first_cart.dish and first_cart.dish.category and first_cart.dish.category.restaurant:
        restaurant = first_cart.dish.category.restaurant
        promotions = [first_cart.dish.promotion.name] if first_cart.dish.promotion else []
    else:
        restaurant = None
        promotions = []


    delivery_info = calculate_delivery_time(first_cart) if first_cart else {
        'delivery_time': 0,
        'delivery_price': Decimal('0.00'),
        'total_price': total_price
    }

    return {
        'total_quantity': total_quantity,
        'delivery_fee': delivery_info['delivery_price'],
        'total_price': delivery_info['total_price'],
        'delivery_time': delivery_info['delivery_time'],
        'items': items,
        'restaurant': {
            'id': restaurant.id if restaurant else None,
            'name': restaurant.name if restaurant else None,
            'promotions': promotions
        },
        'status': 'pending'
    }