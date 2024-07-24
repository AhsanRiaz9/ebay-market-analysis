from django.db import models
from .modules import Module


class Permission(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=50)
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='permissions') 


    class Meta:
        unique_together = ["name", "code"]  
    
    def __str__(self):
        return f'{self.name}' 