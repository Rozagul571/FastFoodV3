from rest_framework import serializers
from .models import SubCategory, Dish
from apps.restaurants.models import Category
from ..cart.utils import apply_promotion

class SubCategorySerializer(serializers.ModelSerializer):
    parent = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), allow_null=True)

    class Meta:
        model = SubCategory
        fields = ('id', 'name', 'parent', 'restaurant')
        read_only_fields = ('id',)

    def validate_parent(self, parent):
        if parent and not parent.restaurant:
            raise serializers.ValidationError("Parent category must be associated with a restaurant.")
        return parent

    def create(self, validated_data):
        parent = validated_data.get('parent')
        sub_category = super().create(validated_data)
        if parent and not sub_category.restaurant:
            sub_category.restaurant = parent.restaurant
            sub_category.save()
        return sub_category

class DishListSerializer(serializers.ModelSerializer):
    original_price = serializers.DecimalField(max_digits=10, decimal_places=2, source='price', read_only=True)
    promotion_price = serializers.SerializerMethodField()

    class Meta:
        model = Dish
        fields = ('id', 'name', 'price', 'original_price', 'promotion_price')
        read_only_fields = ('id', 'original_price', 'promotion_price')

    def get_promotion_price(self, obj):
        base_price = obj.price
        _, adjusted_quantity = apply_promotion(1, base_price, obj.promotion)
        adjusted_price, _ = apply_promotion(adjusted_quantity, base_price, obj.promotion)
        return adjusted_price

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than zero.")
        return value

class DishDetailSerializer(serializers.ModelSerializer):
    original_price = serializers.DecimalField(max_digits=10, decimal_places=2, source='price', read_only=True)
    promotion_price = serializers.SerializerMethodField()
    promotion = serializers.ChoiceField(choices=(('1+1', '1+1 Aksiya'), ('2+1', '2+1 Aksiya'), ('free_delivery', 'Free Delivery')), required=False, allow_null=True)
    promotion_name = serializers.SerializerMethodField()
    # image = serializers.CharField(max_length=255, required=False, allow_null=True)
    restaurant = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Dish
        fields = ('id', 'name', 'price', 'original_price', 'promotion_price', 'promotion', 'promotion_name', 'category', 'restaurant')
        read_only_fields = ('id', 'original_price', 'promotion_price', 'promotion_name', 'restaurant')

    def get_promotion_price(self, obj):
        base_price = obj.price
        quantity = 1
        _, adjusted_quantity = apply_promotion(quantity, base_price, obj.promotion)
        adjusted_price, _ = apply_promotion(adjusted_quantity, base_price, obj.promotion)
        return adjusted_price if adjusted_quantity > 0 else base_price

    def get_promotion_name(self, obj):
        return obj.promotion if obj.promotion else None

    def validate_category(self, category):
        if not category.restaurant:
            raise serializers.ValidationError("Category must be associated with a restaurant.")
        return category

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than zero.")
        return value

    def create(self, validated_data):
        category = validated_data['category']
        validated_data['restaurant'] = category.restaurant
        dish = super().create(validated_data)
        return dish

    def update(self, instance, validated_data):
        instance.image = validated_data.get('image', instance.image)
        instance.promotion = validated_data.get('promotion', instance.promotion)
        instance.save()
        return instance