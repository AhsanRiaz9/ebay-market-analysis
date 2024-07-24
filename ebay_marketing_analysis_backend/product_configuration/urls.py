from django.urls import path
from .views import LoadProductConfiguration, DownloadEbayCondtions, DownloadEbayLocations

urlpatterns = [
    path('load_configuration/<int:category_id>/', LoadProductConfiguration.as_view()),
    path('download_ebay_conditions/', DownloadEbayCondtions.as_view()),
    path('load_ebay_locations/', DownloadEbayLocations.as_view()),
]