from django.db import models
from role_management.models import CustomUser

class SpecificProductProcess(models.Model):
    url = models.TextField()
    notes = models.TextField()
    is_sold_listing = models.BooleanField(default=False)
    status = models.CharField(max_length=30, default="")
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
