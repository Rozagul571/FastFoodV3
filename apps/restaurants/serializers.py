from rest_framework import serializers
from django.contrib.gis.geos import Point
from apps.dishes.models import SubCategory
from apps.restaurants.models import Restaurant, Promotion, Category
from django.core.exceptions import ValidationError

class PromotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promotion
        fields = ('id', 'name')
        read_only_fields = ('id',)

class CategorySerializer(serializers.ModelSerializer):
    restaurant = serializers.PrimaryKeyRelatedField(queryset=Restaurant.objects.all(), required=True)

    class Meta:
        model = Category
        fields = ('id', 'name', 'parent', 'restaurant')
        read_only_fields = ('id',)

    def validate(self, data):
        restaurant_id = data.get('restaurant')
        if not Restaurant.objects.filter(id=restaurant_id.id).exists():
            raise ValidationError({"restaurant": ["Restaurant does not exist."]})
        if data.get('parent') and data['parent'].restaurant != restaurant_id:
            raise ValidationError({"parent": ["Parent category must belong to the same restaurant."]})
        return data

    def create(self, validated_data):
        restaurant = validated_data.pop('restaurant')
        category = Category(restaurant=restaurant, **validated_data)
        category.save()
        return category

class RestaurantSerializer(serializers.ModelSerializer):
    latitude = serializers.FloatField(write_only=True)
    longitude = serializers.FloatField(write_only=True)
    promotions = PromotionSerializer(many=True, required=False)
    delivery_time = serializers.SerializerMethodField()

    class Meta:
        model = Restaurant
        fields = ('id', 'name', 'latitude', 'longitude', 'location', 'promotions', 'delivery_time')
        read_only_fields = ('id', 'location', 'delivery_time')

    # def get_delivery_time(self, obj):
    #     user_address = self.context['request'].user.addresses.order_by('-id').first()
    #     if user_address and user_address.location:
    #         return calculate_delivery_time(obj, user_address.location)
    #     return 30

    def create(self, validated_data):
        promotions_data = validated_data.pop('promotions', [])
        lat = validated_data.pop('latitude')
        lon = validated_data.pop('longitude')
        validated_data['location'] = Point(lon, lat)

        try:
            restaurant = Restaurant.objects.create(**validated_data)
        except Exception as e:
            raise ValidationError(f"Failed to create restaurant: {str(e)}")

        for promotion_data in promotions_data:
            if promotion_data.get('name'):
                promotion, created = Promotion.objects.get_or_create(name=promotion_data['name'])
                if restaurant:
                    restaurant.promotions.add(promotion)
                else:
                    raise ValidationError("Restaurant creation failed, cannot add promotions.")
            else:
                raise ValidationError("Promotion name is required.")

        return restaurant

    def validate(self, data):
        if not data.get('latitude') or not data.get('longitude'):
            raise ValidationError("Latitude and longitude are required.")
        return data

class SubCategorySerializer(serializers.ModelSerializer):
    parent = serializers.PrimaryKeyRelatedField(queryset=Category.objects.filter(parent=None))
    restaurant = serializers.PrimaryKeyRelatedField(queryset=Restaurant.objects.all(), required=True)

    class Meta:
        model = SubCategory
        fields = ('id', 'name', 'parent', 'restaurant')
        read_only_fields = ('id',)

    def validate_parent(self, parent):
        if parent.restaurant is None:
            raise ValidationError("Parent category must be associated with a restaurant.")
        return parent

    def create(self, validated_data):
        restaurant = validated_data.pop('restaurant')
        parent = validated_data['parent']
        if parent.restaurant != restaurant:
            raise ValidationError("Restaurant must match parent's restaurant.")
        sub_category = super().create(validated_data)
        sub_category.restaurant = restaurant
        sub_category.save()
        return sub_category
