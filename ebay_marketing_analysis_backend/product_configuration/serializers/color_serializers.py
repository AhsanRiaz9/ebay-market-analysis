from rest_framework import serializers
from product_configuration.models import ColorCategory

class ColorCategorySerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    
    class Meta:
        model = ColorCategory
        fields = ('id', 'name',)

    def get_name(self, obj):
        return obj.color.name
