from django.db import models
from .permissions import Permission


class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)
    permissions = models.ManyToManyField(Permission)
    

    def __str__(self):
        return self.name