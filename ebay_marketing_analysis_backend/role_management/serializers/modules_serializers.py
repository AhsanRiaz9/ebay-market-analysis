from role_management.models import Module
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

class ModuleSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Module
        fields= ['id', 'name']
        
 
        


        