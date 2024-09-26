from django.db import models
from product_configuration.models import Category
from .ebay_store import EbayStore

class EbayStoreProduct(models.Model):
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_fee = models.DecimalField(max_digits=10, decimal_places=2)
    ebay_item_id = models.CharField(max_length=100)
    product_url = models.CharField(unique=True, max_length=255)
    image = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    ebay_store = models.ForeignKey(EbayStore, on_delete=models.SET_NULL, null=True)
    sold_date = models.DateField(null=True)
    is_sold_listing = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
