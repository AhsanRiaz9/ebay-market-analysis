from django.urls import path
from competitor_analysis.views import DownloadEbayStoreView

urlpatterns = [
    path('download_ebay_store/', DownloadEbayStoreView.as_view()),
]
