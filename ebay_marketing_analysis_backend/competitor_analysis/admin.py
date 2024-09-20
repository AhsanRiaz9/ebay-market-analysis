from django.contrib import admin
from .models import EbayStore, StoreCategory, EbayStoreProduct

# Register your models here.
admin.site.register(EbayStore)
admin.site.register(StoreCategory)
admin.site.register(EbayStoreProduct)

