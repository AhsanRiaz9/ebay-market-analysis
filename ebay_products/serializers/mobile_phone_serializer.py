from rest_framework import serializers
from ebay_products.models import MobilePhone

class MobilePhoneSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = MobilePhone
        fields = '__all__'
    
    def to_representation(self, instance):
        response = super().to_representation(instance) 
        response['category'] = instance.category.ebay_category_id if instance.category else ''
        response['product_model'] = instance.product_model.product_model.name if instance.product_model else ''
        response['brand'] = instance.brand.brand.name if instance.brand else ''
        response['color'] = instance.color.color.name if instance.color else ''
        response['storage'] = instance.storage.value if instance.storage else ''
        response['lock_status'] = instance.lock_status.name if instance.lock_status else ''
        response['condition'] = instance.condition.ebay_condition_id if instance.condition else ''
        response['location'] = instance.location.country if instance.location else ''
        return response