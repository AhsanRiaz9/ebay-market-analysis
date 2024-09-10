from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('admin/', admin.site.urls),
    # roles management
    path('', include('role_management.urls')),
    # ebay scraping tool
    path('api-auth/', include('rest_framework.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('product_configuration/', include('product_configuration.urls')),
    path('ebay_products/', include('ebay_products.urls')),
    path('scraping_scheduler/', include('scraping_scheduler.urls')),
    # competitor anaysis
    path('competitor_analysis/', include('competitor_analysis.urls')),
]
