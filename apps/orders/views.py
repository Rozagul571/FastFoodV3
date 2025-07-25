from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Order
from .serializers import OrderSerializer
from apps.users.permissions import RoleBasedPermission

class OrderCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated, RoleBasedPermission.with_roles(['customer'])]
    serializer_class = OrderSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            order = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OrderListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated, RoleBasedPermission.with_roles(['customer', 'admin'])]
    serializer_class = OrderSerializer

    def get_queryset(self):
        if self.request.user.role == 'admin':
            return Order.objects.all()
        return Order.objects.filter(user=self.request.user)

class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, RoleBasedPermission.with_roles(['customer', 'admin'])]
    serializer_class = OrderSerializer

    def get_queryset(self):
        if self.request.user.role == 'admin':
            return Order.objects.all()
        return Order.objects.filter(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": f"Order {instance.id} cancelled"}, status=status.HTTP_200_OK)