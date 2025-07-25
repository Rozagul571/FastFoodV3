from .models import Order

def get_orders(request):
    if request.user.role in ['admin', 'waiter']:
        return Order.objects.all()
    return Order.objects.filter(user=request.user)

def get_order_by_id(order_id):
    return Order.objects.filter(id=order_id)