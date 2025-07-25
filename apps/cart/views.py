from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Cart
from .serializers import CartSerializer, CartUpdateQuantitySerializer
from apps.users.permissions import RoleBasedPermission

class CartListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, RoleBasedPermission.with_roles(['customer', 'admin'])]
    serializer_class = CartSerializer

    def get_queryset(self):
        return Cart.objects.select_related('dish').filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class CartUpdateView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated, RoleBasedPermission.with_roles(['customer', 'admin'])]
    serializer_class = CartSerializer
    queryset = Cart.objects.select_related('dish').all()

    def get_object(self):
        return self.get_queryset().filter(user=self.request.user, dish__id=self.request.data.get('dish')).first()

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance is None:
            return Response({"error": "Cart item not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CartUpdateQuantityView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CartUpdateQuantitySerializer
    queryset = Cart.objects.select_related('dish').all()

    def get_object(self):
        return self.get_queryset().filter(user=self.request.user).first()

class CartClearView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Cart.objects.all()

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        count = self.get_queryset().count()
        if count == 0:
            return Response({"error": "No cart found for this user."}, status=status.HTTP_404_NOT_FOUND)
        self.get_queryset().delete()
        return Response({"message": f"All {count} carts cleared for this user."}, status=status.HTTP_200_OK)

class CartItemDeleteView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Cart.objects.all()

    def get_object(self):
        return self.get_queryset().filter(user=self.request.user, pk=self.kwargs['pk']).first()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance is None:
            return Response({"error": "Cart item not found."}, status=status.HTTP_404_NOT_FOUND)
        instance.delete()
        return Response({"message": f"Cart item {self.kwargs['pk']} deleted."}, status=status.HTTP_200_OK)