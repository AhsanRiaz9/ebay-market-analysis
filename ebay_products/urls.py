from django.urls import path
from .views import DownloadProduct

urlpatterns = [
    path('download_products/<int:category_id>/', DownloadProduct.as_view()),
]
