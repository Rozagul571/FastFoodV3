# from ipaddress import ip_address
#
# from rest_framework import generics, status
# from rest_framework.response import Response
# from apps.users.permissions import IsUser, IsUserOrGuest
# from apps.cart.models import Cart
# from apps.cart.serializers import CartSerializer, CartItemSerializer
# from apps.cart.services import add_to_cart, remove_from_cart, checkout_cart, get_cart, get_user_ip
# from apps.users.serializers import UserLocationSerializer
#
#
# class CartView(generics.ListCreateAPIView):
#     queryset = Cart.objects.all()
#     serializer_class = CartSerializer
#     permission_classes = (IsUserOrGuest,)
#
#     def get_queryset(self):
#         return get_cart(self.request)
#
#     def list(self, request, *args, **kwargs):
#         cart_items = self.get_queryset()
#         if not cart_items.exists():
#             return Response({
#                 "cart_id": None,
#                 "restaurant_id": None,
#                 "restaurant_name": None,
#                 "items": [],
#                 "total_price": 0.00,
#                 "total_quantity": 0
#             }, status=status.HTTP_200_OK)
#         serializer = self.get_serializer(cart_items, many=True)
#         return Response({
#             "cart_id": cart_items.first().id,
#             "restaurant_id": cart_items.first().restaurant.id,
#             "restaurant_name": str(cart_items.first().restaurant),
#             "items": serializer.data,
#             "total_price": sum(float(item.dish.price * item.quantity) for item in cart_items),
#             "total_quantity": sum(item.quantity for item in cart_items)
#         }, status=status.HTTP_200_OK)
#
#     def create(self, request, *args, **kwargs):
#         serializer = CartItemSerializer(data=request.data, context={'request': request})
#         serializer.is_valid(raise_exception=True)
#         dish_id = serializer.validated_data['dish'].id
#         quantity = serializer.validated_data['quantity']
#         ip_address = get_user_ip(request)
#
#         cart, error = add_to_cart(request, dish_id, quantity, ip_address)
#         if error:
#             return Response({"message": error}, status=status.HTTP_400_BAD_REQUEST)
#         return Response({
#             "cart_id": cart.id,
#             **CartItemSerializer(cart, context={'request': request}).data
#         }, status=status.HTTP_201_CREATED)
#
#
# class CartAddView(generics.CreateAPIView):
#     queryset = Cart.objects.all()
#     serializer_class = CartItemSerializer
#     permission_classes = (IsUserOrGuest,)
#
#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data, context={'request': request})
#         serializer.is_valid(raise_exception=True)
#         dish_id = serializer.validated_data['dish'].id
#         quantity = serializer.validated_data['quantity']
#         ip_address = get_user_ip(request)
#
#         cart, error = add_to_cart(request, dish_id, quantity, ip_address)
#         if error:
#             return Response({"message": error}, status=status.HTTP_400_BAD_REQUEST)
#         return Response({
#             "cart_id": cart.id,
#             **CartItemSerializer(cart, context={'request': request}).data
#         }, status=status.HTTP_201_CREATED)
#
#
# class CartRemoveView(generics.CreateAPIView):
#     queryset = Cart.objects.all()
#     permission_classes = (IsUserOrGuest,)
#     serializer_class = None
#
#     def create(self, request, *args, **kwargs):
#         dish_ids = request.data.get('dish_ids', [])
#         success, error = remove_from_cart(request, dish_ids)
#         if error:
#             return Response({"message": error}, status=status.HTTP_400_BAD_REQUEST)
#         return Response({"message": "Tanlangan taomlar savatdan o'chirildi"}, status=status.HTTP_200_OK)
#
#
# class CartCheckoutView(generics.CreateAPIView):
#     queryset = Cart.objects.all()
#     serializer_class = UserLocationSerializer
#     permission_classes = (IsUser,)
#
#     def create(self, request, *args, **kwargs):
#         discount = float(request.data.get('discount', 0.00))
#         payment_method = request.data.get('payment_method', 'cash')
#         location_data = {'latitude': request.data.get('latitude'), 'longitude': request.data.get('longitude')}
#         location = None
#         if location_data['latitude'] and location_data['longitude']:
#             serializer = self.get_serializer(data=location_data)
#             serializer.is_valid(raise_exception=True)
#             location = serializer.validated_data['location']
#         order, error = checkout_cart(request, discount, payment_method, location)
#         if error:
#             return Response({"message": error}, status=status.HTTP_400_BAD_REQUEST)
#         return Response({
#             "order_id": order.id,
#             "restaurant_id": order.restaurant.id,
#             "restaurant_name": order.restaurant.name,
#             "status": order.get_status_display(),
#             "subtotal": order.subtotal,
#             "delivery_fee": order.delivery_fee,
#             "payment_method": order.payment_method,
#             "distance_km": order.distance_km,
#             "total_price": order.total,
#             "estimated_time": order.estimated_time
#         }, status=status.HTTP_201_CREATED)