from django.core.exceptions import ObjectDoesNotExist
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.pagination import PageNumberPagination
from rest_framework_simplejwt.serializers import ValidationError
from apps.restaurants.serializers import RestaurantSerializer, CategorySerializer
from apps.restaurants.models import Restaurant, Category
from apps.users.permissions import IsAdminOrRestaurantRole

class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = None

class CategoryListCreateView(generics.ListCreateAPIView):
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrRestaurantRole]
    pagination_class = CustomPagination

    def get_queryset(self):
        return Category.objects.all()

    def perform_create(self, serializer):
        try:
            serializer.save()
        except ObjectDoesNotExist as e:
            raise ValidationError({"restaurant": ["Invalid restaurant ID or no restaurant exists."]})

class RestaurantListCreateView(generics.ListCreateAPIView):
    serializer_class = RestaurantSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        if not self.request.user.is_authenticated or self.request.user.role == 'customer':
            return Restaurant.objects.all()
        return Restaurant.objects.all()

    def perform_create(self, serializer):
        try:
            serializer.save()
        except Exception as e:
            raise ValidationError(f"Failed to create restaurant: {str(e)}")

class RestaurantByCategoryView(generics.ListAPIView):
    serializer_class = RestaurantSerializer
    permission_classes = [AllowAny]
    pagination_class = CustomPagination

    def get_queryset(self):
        category_id = self.kwargs.get('category_id')
        category = Category.objects.filter(id=category_id, parent=None).first()
        if not category:
            raise ValidationError("Category doesnt exist or is not a root category.")
        return Restaurant.objects.filter(categories__id=category.id)