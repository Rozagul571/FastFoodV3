from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from .models import SubCategory, Dish
from .serializers import SubCategorySerializer, DishDetailSerializer
from django.shortcuts import get_object_or_404
from django.core.cache import cache
from apps.users.permissions import RoleBasedPermission

class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'

class SubCategoryListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, RoleBasedPermission.with_roles(['admin', 'restaurantManager', 'oshpaz'])]
    serializer_class = SubCategorySerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        return SubCategory.objects.all()

    def perform_create(self, serializer):
        serializer.save()

class DishListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, RoleBasedPermission.with_roles(['admin', 'restaurantManager', 'oshpaz'])]
    pagination_class = CustomPagination
    serializer_class = DishDetailSerializer

    def get_queryset(self):
        return Dish.objects.select_related('category__restaurant').all()

    def perform_create(self, serializer):
        serializer.save()

class DishDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, RoleBasedPermission.with_roles(['admin', 'restaurantManager', 'oshpaz'])]
    serializer_class = DishDetailSerializer

    def get_queryset(self):
        return Dish.objects.select_related('category__restaurant').all()

    def get_object(self):
        obj = get_object_or_404(Dish, id=self.kwargs['id'])
        cache_key = f"dish_{obj.id}"
        if not cache.get(cache_key):
            cache.set(cache_key, obj, timeout=3600)
        return obj

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": f"Dish {instance.name} deleted"}, status=status.HTTP_200_OK)