from asyncio import Condition
from django.contrib import admin
from .models import Category, Brand, BrandCategory, Color, ColorCategory, LockStatus, ProductModel, ProductModelCategory, Storage, Condition, ConditionCategory, Filter, FilterCategory, Location

# Register your models here.
admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(BrandCategory)
admin.site.register(Color)
admin.site.register(ColorCategory)
admin.site.register(LockStatus)
admin.site.register(ProductModel)
admin.site.register(ProductModelCategory)
admin.site.register(Storage)
admin.site.register(Condition)
admin.site.register(Filter)
admin.site.register(FilterCategory)
admin.site.register(Location)
admin.site.register(ConditionCategory)
