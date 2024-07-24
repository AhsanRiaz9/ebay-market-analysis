from django.db import models


class Location(models.Model):
    domain = models.CharField(max_length=30, unique=True)
    country = models.CharField(max_length=30, null=True)

    def __str__(self):
        return f'{self.country}::({self.domain})'