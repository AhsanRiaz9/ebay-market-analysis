from django.db import models
from django.contrib.auth.models import AbstractUser
from role_management.manager import UserManager
from .roles import Role


class CustomUser(AbstractUser):
    username = None
    name = models.CharField(max_length=100, default=1, null=True, blank= True)
    phone_number = models.CharField(max_length=15, null=True, blank= True)
    email = models.EmailField(unique=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, null=True, blank= True) 
    
    is_superuser= models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    objects = UserManager()
        
        
    def __str__(self):
        return self.email









