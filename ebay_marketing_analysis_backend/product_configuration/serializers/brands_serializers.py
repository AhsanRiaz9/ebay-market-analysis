from rest_framework import serializers
from product_configuration.models import BrandCategory

class BrandCategorySerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    
    class Meta:
        model = BrandCategory
        fields = ('id', 'name', )

    def get_name(self, obj):
        return obj.brand.name
