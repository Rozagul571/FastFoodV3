from django.urls import path
from .views import CategoryListCreateView, RestaurantListCreateView, RestaurantByCategoryView

urlpatterns = [
    path('categories/', CategoryListCreateView.as_view(), name='category-list-create'),
    path('', RestaurantListCreateView.as_view(), name='restaurant-list-create'),
    path('category/<int:category_id>/', RestaurantByCategoryView.as_view(), name='restaurant-by-category'),
#     path('<int:category>/categories/', RestaurantByCategoryView.as_view(), name='restaurant-by-category'),
]

