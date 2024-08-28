from django.db import models
from .ebay_store import EbayStore
from product_configuration.models import Category

class StoreCategory(models.Model):
    ebay_store = models.ForeignKey(EbayStore, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
