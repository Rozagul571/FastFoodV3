from rest_framework import serializers
from .models import Order, OrderItem
from apps.cart.models import Cart
from apps.utils import calculate_order_totals
from apps.cart.utils import clear_cart
from django.contrib.gis.geos import Point
from django.db import transaction
from apps.users.models import Address

class OrderItemSerializer(serializers.ModelSerializer):
    dish_name = serializers.CharField(source='dish.name', read_only=True)
    price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = OrderItem
        fields = ('id', 'dish', 'dish_name', 'quantity', 'price')
        read_only_fields = ('id', 'dish_name', 'price')

class OrderSerializer(serializers.ModelSerializer):
    address_id = serializers.PrimaryKeyRelatedField(queryset=Address.objects.all(), source='address', required=True)
    items = OrderItemSerializer(many=True, read_only=True)
    restaurant = serializers.SerializerMethodField()
    total_quantity = serializers.IntegerField(read_only=True)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    total_all_quantities = serializers.IntegerField(read_only=True)
    total_all_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Order
        fields = ('id', 'user', 'address_id', 'restaurant', 'items', 'status', 'total_quantity', 'total_price',
                  'total_all_quantities', 'total_all_price')
        read_only_fields = ('id', 'user', 'items', 'status', 'total_quantity', 'total_price',
                            'total_all_quantities', 'total_all_price')

    def get_restaurant(self, obj):
        if obj.restaurant is not None:
            return {'id': obj.restaurant.id, 'name': obj.restaurant.name}
        return None

    def validate(self, data):
        address_id = data.get('address')
        if address_id is None:
            raise serializers.ValidationError({"address_id": "An address ID is required."})
        return data

    def create(self, validated_data):
        user = self.context['request'].user
        address = validated_data.pop('address')
        cart = Cart.objects.get(user=user)
        if cart.dish is None:
            raise serializers.ValidationError({"error": "Cart is empty"})
        if not cart.restaurant:
            raise serializers.ValidationError({"error": "Cart restaurant is not set"})

        with transaction.atomic():
            order = Order.objects.create(user=user, address=address, restaurant=cart.restaurant)
            totals = calculate_order_totals(cart)
            # Faqat bitta dish uchun OrderItem yaratamiz
            order_items = [
                OrderItem(order=order, dish=cart.dish, quantity=cart.quantity, price=cart.dish.price * cart.quantity)
            ]
            OrderItem.objects.bulk_create(order_items)
            clear_cart(cart)

        self._total_quantity = totals['total_quantity']
        self._total_price = totals['total_price']
        self._total_all_quantities = totals['total_quantity']
        self._total_all_price = totals['total_price']

        return order

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.address is not None:
            representation['address_id'] = instance.address.id
        representation['total_quantity'] = getattr(self, '_total_quantity', 0)
        representation['total_price'] = float(getattr(self, '_total_price', 0.00))
        representation['total_all_quantities'] = getattr(self, '_total_all_quantities', 0)
        representation['total_all_price'] = float(getattr(self, '_total_all_price', 0.00))
        return representation