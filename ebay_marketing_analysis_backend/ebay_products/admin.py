from django.contrib import admin
from .models import MobilePhone, ActiveMobilePhone, ProductRankCounter

# Register your models here.
admin.site.register(MobilePhone)
admin.site.register(ActiveMobilePhone)
admin.site.register(ProductRankCounter)
