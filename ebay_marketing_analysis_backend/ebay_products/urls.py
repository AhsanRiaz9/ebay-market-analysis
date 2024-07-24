from django.urls import path
from .views import DownloadProductView, MobilePhoneListView

urlpatterns = [
    path('download_products/<int:category_id>/', DownloadProductView.as_view()),
    path('mobile_phones/', MobilePhoneListView.as_view()),
]
