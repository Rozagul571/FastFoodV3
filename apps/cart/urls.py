from django.urls import path
from .views import CartListCreateView, CartUpdateView, CartUpdateQuantityView, CartClearView, CartItemDeleteView

urlpatterns = [
    path('', CartListCreateView.as_view(), name='cart-list-create'),
    path('update/', CartUpdateView.as_view(), name='cart-update'),
    path('update-quantity/', CartUpdateQuantityView.as_view(), name='cart-update-quantity'),
    path('clear/', CartClearView.as_view(), name='cart-clear'),
    path('<int:pk>/delete/', CartItemDeleteView.as_view(), name='cart-item-delete'),
]