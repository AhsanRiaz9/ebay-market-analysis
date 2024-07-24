from django.db import models
from .categories import Category

class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return f'{self.name}'

class BrandCategory(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('brand', 'category',)
        
    def __str__(self):
        return f'{self.category}:{self.brand.name}'
