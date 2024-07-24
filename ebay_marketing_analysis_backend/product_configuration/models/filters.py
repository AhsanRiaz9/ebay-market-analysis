from django.db import models
from .categories import Category


class Filter(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f'{self.name}'

class FilterCategory(models.Model):
    filter = models.ForeignKey(Filter, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ('filter', 'category',)
        
    def __str__(self):
        return f'{self.category}:{self.filter.name}'
 
    
"""
https://www.ebay.com.au/b/Mobile-Phones/9355/bn_504059?Features=Facial%2520Recognition&rt=nc&_fsrp=0&LH_BIN=1&_sacat=9355&Storage%2520Capacity=64%2520GB%7C128%2520GB&Model=Apple%2520iPhone%252012%7CApple%2520iPhone%252011&LH_Complete=1&LH_ItemCondition=2020%7C3000%7C1500&LH_Sold=1&Colour=Green%7CYellow&mag=1
"""

