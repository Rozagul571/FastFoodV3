from django.urls import path
from .views import SubCategoryListCreateView, DishListCreateView, DishDetailView

urlpatterns = [
    path('subcategories/', SubCategoryListCreateView.as_view(), name='subcategory-list-create'),
    path('', DishListCreateView.as_view(), name='dish-list-create'),
    path('<int:id>/', DishDetailView.as_view(), name='dish-detail'),
]