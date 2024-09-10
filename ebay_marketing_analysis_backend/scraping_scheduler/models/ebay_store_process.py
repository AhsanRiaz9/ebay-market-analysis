from django.db import models
from role_management.models import CustomUser
from competitor_analysis.models import EbayStore

class EbayStoreProcess(models.Model):
    ebay_store = models.ForeignKey(EbayStore, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=30, default="")
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
