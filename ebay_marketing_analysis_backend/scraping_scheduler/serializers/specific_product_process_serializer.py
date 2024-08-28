from rest_framework import serializers
from scraping_scheduler.models import SpecificProductProcess
from settings.utilis.formatters import date_format

class SpecificProductProcessSerializer(serializers.ModelSerializer):
        
    class Meta:
        model = SpecificProductProcess
        fields = '__all__'

    def to_representation(self, instance):
        response =  super().to_representation(instance)
        response['created_at'] = date_format(instance.created_at)
        response['created_by'] = instance.created_by.name if instance.created_by else ''
        return response
    
