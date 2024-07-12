from django.db import models

class Category(models.Model):
    name = models.TextField()
    ebay_category_id = models.IntegerField(unique=True, db_index=True)  
    
    class Meta:
        indexes = [
            models.Index(fields=['ebay_category_id'])
        ]

    def __str__(self):
        return f'{self.ebay_category_id}:{self.name}'