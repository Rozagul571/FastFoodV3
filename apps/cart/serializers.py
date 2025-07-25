from rest_framework import serializers
from .models import Cart
from apps.dishes.models import Dish
from .utils import calculate_cart_totals, apply_promotion
from rest_framework.pagination import PageNumberPagination

class CartPagination(PageNumberPagination):
    page_size = 10
    max_page_size = 100

class CartSerializer(serializers.ModelSerializer):
    dish = serializers.PrimaryKeyRelatedField(queryset=Dish.objects.all())
    quantity = serializers.IntegerField(min_value=1)

    class Meta:
        model = Cart
        fields = ('id', 'user', 'dish', 'quantity', 'total_quantity', 'restaurant')
        read_only_fields = ('id', 'user', 'total_quantity', 'restaurant')

    def validate(self, data):
        user = self.context['request'].user
        dish = data.get('dish')
        if Cart.objects.filter(user=user, dish=dish).exists():
            raise serializers.ValidationError({"dish": "This dish is already in your cart. Use PATCH to update quantity."})
        return data

    def create(self, validated_data):
        user = self.context['request'].user
        dish = validated_data['dish']
        quantity = validated_data['quantity']
        cart = Cart.objects.create(user=user, dish=dish, quantity=quantity, restaurant=dish.restaurant)
        return cart

    def update(self, instance, validated_data):
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.save()
        return instance

    def to_representation(self, instance):
        request = self.context.get('request')
        is_get_request = False
        if request is not None and request.method == 'GET':
            is_get_request = True
        if is_get_request and isinstance(instance, list) and len(instance) > 0:
            carts_data = []
            total_quantity = 0
            total_price = 0.0
            for cart in instance:
                if cart.dish is not None:
                    base_price = cart.dish.price * cart.quantity
                    promotion = cart.dish.promotion.name if cart.dish.promotion else None
                    adjusted_price, promotion_quantity = apply_promotion(cart.quantity, base_price, promotion)
                    restaurant = cart.restaurant
                    carts_data.append({
                        'id': cart.id,
                        'user': cart.user.id,
                        'dish': cart.dish.id,
                        'quantity': cart.quantity,
                        'promotion_quantity': promotion_quantity,
                        'price': float(base_price),
                        'promotion': promotion,
                        'restaurant_id': restaurant.id if restaurant else None,
                        'restaurant_name': restaurant.name if restaurant else None
                    })
                    total_quantity += promotion_quantity
                    total_price += base_price
                else:
                    carts_data.append({
                        'id': cart.id,
                        'user': cart.user.id,
                        'dish': None,
                        'quantity': cart.quantity,
                        'promotion_quantity': cart.quantity,
                        'price': 0.0,
                        'promotion': None,
                        'restaurant_id': None,
                        'restaurant_name': None
                    })
                    total_quantity += cart.quantity
                    total_price += 0.0
            return {
                'count': len(instance),
                'next': None,
                'previous': None,
                'results': carts_data,
                'total_quantity': total_quantity,
                'total_price': float(total_price)
            }
        else:
            if instance.dish is not None:
                base_price = instance.dish.price * instance.quantity
                promotion = instance.dish.promotion.name if instance.dish.promotion else None
                adjusted_price, promotion_quantity = apply_promotion(instance.quantity, base_price, promotion)
                restaurant = instance.restaurant
                return {
                    'id': instance.id,
                    'user': instance.user.id,
                    'dish': instance.dish.id,
                    'quantity': instance.quantity,
                    'promotion_quantity': promotion_quantity,
                    'price': float(base_price),
                    'promotion': promotion,
                    'restaurant_id': restaurant.id if restaurant else None,
                    'restaurant_name': restaurant.name if restaurant else None
                }
            else:
                return {
                    'id': instance.id,
                    'user': instance.user.id,
                    'dish': None,
                    'quantity': instance.quantity,
                    'promotion_quantity': instance.quantity,
                    'price': 0.0,
                    'promotion': None,
                    'restaurant_id': None,
                    'restaurant_name': None
                }

class CartUpdateQuantitySerializer(serializers.ModelSerializer):
    quantity = serializers.IntegerField(min_value=1, help_text="The number of items to set for the cart minimum 1")

    class Meta:
        model = Cart
        fields = ('quantity',)
        extra_kwargs = {
            'quantity': {'required': True},
        }

    def validate_quantity(self, value):
        if value < 1:
            raise serializers.ValidationError("Quantity must be at least 1")
        return value

    def update(self, instance, validated_data):
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.save()
        return instance