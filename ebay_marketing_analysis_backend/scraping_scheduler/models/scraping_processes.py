from django.db import models
from product_configuration.models import Category, Condition

# Create your models here.
class ScrapingProcess(models.Model):
    category = models.name = models.OneToOneField(Category, on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now_add=True)
    

class MobileScrapingProcess(models.Model):
    scraping_process = models.ForeignKey(ScrapingProcess, on_delete=models.CASCADE)
    condition = models.ForeignKey(Condition, on_delete=models.CASCADE)
    mobile_model = models.CharField(max_length=255, blank=True, default='')
    is_completed = models.BooleanField(default=False)
    is_sold_listing = models.BooleanField(default=True)
    
    class Meta:
        unique_together = ('scraping_process', 'condition', 'is_sold_listing')

