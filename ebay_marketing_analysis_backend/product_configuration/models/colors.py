from django.db import models
from .categories import Category


class Color(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return f'{self.name}'

class ColorCategory(models.Model):
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('color', 'category',)
        
    def __str__(self):
        return f'{self.category}:{self.color.name}'