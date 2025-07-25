from django.urls import path
from .views import RegisterView, AddressCreateView, AddressListView, AddressDetailView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('addresses/', AddressCreateView.as_view(), name='address-create'),
    path('addresses/list/', AddressListView.as_view(), name='address-list'),
    path('addresses/<int:pk>/', AddressDetailView.as_view(), name='address-detail'),
]