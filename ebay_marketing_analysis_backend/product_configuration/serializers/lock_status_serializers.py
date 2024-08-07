from rest_framework import serializers
from product_configuration.models import LockStatus

class LockStatusSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = LockStatus
        fields = '__all__'
