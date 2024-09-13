from django.contrib import admin
from .models import EbayStore, StoreCategory

# Register your models here.
admin.site.register(EbayStore)
admin.site.register(StoreCategory)
