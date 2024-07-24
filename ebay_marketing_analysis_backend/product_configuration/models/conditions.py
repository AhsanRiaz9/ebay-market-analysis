from django.db import models
from .categories import Category

class Condition(models.Model):
    name = models.CharField(max_length=50)
    ebay_condition_id = models.IntegerField(unique=True, db_index=True)
    
    def __str__(self):
        return f'{self.name}'

class ConditionCategory(models.Model):
    condition = models.ForeignKey(Condition, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)    
    
    class Meta:
        unique_together = ('condition', 'category',)

    def __str__(self):
        return f'{self.category}:{self.condition.name}:{self.condition.ebay_condition_id}'