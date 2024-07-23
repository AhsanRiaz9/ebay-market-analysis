from django.contrib import admin
from .models import MobileScrapingProcess, ScrapingProcess

# Register your models here.
admin.site.register(MobileScrapingProcess)
admin.site.register(ScrapingProcess)