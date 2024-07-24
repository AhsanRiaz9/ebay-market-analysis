from django.db import models
from .categories import Category

class ProductModel(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return f'{self.name}'


class ProductModelCategory(models.Model):
    product_model = models.ForeignKey(ProductModel, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('product_model', 'category',)
        
    def __str__(self):
        return f'{self.category}:{self.product_model.name}'