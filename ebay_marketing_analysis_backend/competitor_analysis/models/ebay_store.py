from django.db import models

# Create your models here.
class EbayStore(models.Model):
    name = models.CharField(max_length=100, unique=True)
    ebay_store_id = models.CharField(max_length=100, unique=True)
    url = models.TextField()
    feedback = models.DecimalField(max_digits=10, decimal_places=2)
    items_sold = models.BigIntegerField()
    followers = models.BigIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} - {self.ebay_store_id}'
