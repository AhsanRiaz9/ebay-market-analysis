from django.urls import path, include
from scraping_scheduler.views import SpecificProductsProcessView

urlpatterns = [
    path('specific_product_processes/', SpecificProductsProcessView.as_view()),
]