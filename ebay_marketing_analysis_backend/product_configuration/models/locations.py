from django.db import models

class Location(models.Model):
    country = models.CharField(max_length=30, unique=True)
    postal_code = models.CharField(default='', max_length=50)
    
    def __str__(self):
        return f'{self.country}::({self.postal_code})'

class EbayDomain(models.Model):
    name = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.name
