from rest_framework import serializers
from product_configuration.models import Condition

class ConditionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Condition
        fields = '__all__'
