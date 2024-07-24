from django.contrib import admin
from .models import CustomUser, Permission, Role, Module

admin.site.register(CustomUser)
admin.site.register(Permission)
admin.site.register(Role)
admin.site.register(Module)


# Register your models here.
