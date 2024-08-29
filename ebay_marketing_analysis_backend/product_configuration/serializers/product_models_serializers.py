from rest_framework import serializers
from product_configuration.models import ProductModelCategory

class ProductModelCategorySerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    
    class Meta:
        model = ProductModelCategory
        fields = ('id', 'name')
    
    def get_name(self, obj):
        return obj.product_model.name

