from django.db import models

# Create your models here.
class EbayStore(models.Model):
    name = models.CharField(max_length=100, default='')
    ebay_store_id = models.CharField(max_length=100, unique=True)
    url = models.TextField()
    feedback = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    items_sold = models.BigIntegerField(default=0)
    followers = models.BigIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    ssn_code = models.CharField(max_length=50, default='')
    category_param = models.CharField(max_length=50, default='store_cat')
    
    def __str__(self):
        return f'{self.name} - {self.ebay_store_id}'
