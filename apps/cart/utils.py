from decimal import Decimal
from apps.cart.models import Cart
from apps.dishes.models import Dish

def clear_cart(cart):
    cart.dish = None
    cart.quantity = 0
    cart.total_quantity = 0
    cart.save()

def apply_promotion(quantity, base_price, promotion=None):
    if not promotion:
        return base_price, quantity
    if promotion == '1+1_aksiya':
        adjusted_quantity = quantity + 1  # Har bir uchun 1 ta bonus
        adjusted_price = base_price
        return adjusted_price, adjusted_quantity
    if promotion == '2+1_aksiya':
        bonus_items = quantity // 2
        adjusted_quantity = quantity + bonus_items
        adjusted_price = base_price
        return adjusted_price, adjusted_quantity
    if promotion == 'free_delivery':
        return base_price, quantity
    return base_price, quantity

def add_dish_to_cart(cart, dish_id, quantity):
    dish = Dish.objects.get(id=dish_id)
    if cart.restaurant is not None and dish.restaurant is not None:
        if cart.restaurant != dish.restaurant:
            raise ValueError("Dish does not belong to the cart's restaurant.")
    cart.dish = dish
    cart.quantity = quantity
    base_price = dish.price * quantity
    adjusted_price, adjusted_quantity = apply_promotion(quantity, base_price, dish.promotion.name if dish.promotion else None)
    cart.total_quantity = adjusted_quantity
    cart.save()

def update_cart_totals(cart):
    if cart.dish is None:
        cart.total_quantity = 0
        cart.save(update_fields=['total_quantity'])
        return {
            'total_quantity': 0,
            'price': Decimal('0.00')
        }
    base_price = cart.dish.price * cart.quantity
    adjusted_price, adjusted_quantity = apply_promotion(cart.quantity, base_price, cart.dish.promotion.name if cart.dish.promotion else None)
    cart.total_quantity = adjusted_quantity
    cart.save(update_fields=['total_quantity'])
    return {
        'total_quantity': adjusted_quantity,
        'price': base_price
    }

def calculate_cart_totals(user):
    carts = Cart.objects.filter(user=user).select_related('dish')
    if not carts.exists():
        return {
            'total_all_quantities': 0,
            'total_all_price': Decimal('0.00')
        }
    total_all_quantities = 0
    total_all_price = Decimal('0.00')
    for cart in carts:
        if cart.dish is not None:
            base_price = cart.dish.price * cart.quantity
            adjusted_price, adjusted_quantity = apply_promotion(cart.quantity, base_price, cart.dish.promotion.name if cart.dish.promotion else None)
            total_all_quantities += adjusted_quantity
            total_all_price += base_price
    return {
        'total_all_quantities': total_all_quantities,
        'total_all_price': total_all_price
    }