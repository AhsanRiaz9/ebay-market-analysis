from django.urls import path
from .views import MobilePhoneListView, DownloadProductView, DownloadSpecificProductsView

urlpatterns = [
    path('mobile_phones/', MobilePhoneListView.as_view()),
    path('download_products/<int:category_id>/', DownloadProductView.as_view()),
    path('download_specific_products/', DownloadSpecificProductsView.as_view()),
]
