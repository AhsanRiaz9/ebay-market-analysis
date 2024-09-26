from django.urls import path
from competitor_analysis.views import DownloadEbayStoreAPIView, DownloadEbayStoreView

urlpatterns = [
    path('download_ebay_store/', DownloadEbayStoreAPIView.as_view()),
]
