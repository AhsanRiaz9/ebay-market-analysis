from django.db import models


class Storage(models.Model):
    value = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return f'{self.value}'