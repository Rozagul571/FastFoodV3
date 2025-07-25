from rest_framework import serializers
from django.contrib.gis.geos import Point
from .models import User, Address

class RegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'phone_number', 'password', 'confirm_password', 'role')
        extra_kwargs = {'password': {'write_only': True}}
        read_only_fields = ('id',)

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({'confirm_password': 'Passwords must match'})
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = User.objects.create_user(
            phone_number=validated_data['phone_number'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            role=validated_data.get('role', 'customer')
        )
        return user

class AddressSerializer(serializers.ModelSerializer):
    latitude = serializers.FloatField(write_only=True)
    longitude = serializers.FloatField(write_only=True)

    class Meta:
        model = Address
        fields = ('id', 'entrance', 'floor', 'apartment', 'latitude', 'longitude', 'user', 'location')
        read_only_fields = ('id', 'user', 'location')

    def create(self, validated_data):
        lat = validated_data.pop('latitude')
        lon = validated_data.pop('longitude')
        validated_data['location'] = Point(lon, lat)
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['latitude'] = instance.location.y if instance.location else None
        rep['longitude'] = instance.location.x if instance.location else None
        return rep