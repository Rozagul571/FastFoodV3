from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView, TokenObtainPairView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api-auth/', include('rest_framework.urls')),
    path('admin/', admin.site.urls),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('users/', include('apps.users.urls')),
    path('restaurants/', include('apps.restaurants.urls')),
    path('orders/', include('apps.orders.urls')),
    path('dishes/', include('apps.dishes.urls')),
    path('cart/', include('apps.cart.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)