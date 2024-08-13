from rest_framework import serializers
from ebay_products.models import MobilePhone, ActiveMobilePhone
from settings.utilis.formatters import custom_datetime_format

class MobilePhoneSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = MobilePhone
        exclude = ('category', 'location', 'scraping_url')
    
    def to_representation(self, instance):
        response = super().to_representation(instance) 
        response['product_model'] = instance.product_model.product_model.name if instance.product_model else ''
        response['brand'] = instance.brand.brand.name if instance.brand else ''
        response['color'] = instance.color.color.name if instance.color else ''
        response['storage'] = instance.storage.value if instance.storage else ''
        response['lock_status'] = instance.lock_status.name if instance.lock_status else ''
        response['condition'] = instance.condition.name if instance.condition else ''
        response['sold_price'] = f'${instance.sold_price}'
        response['shipping_fee'] = f'${instance.shipping_fee}'
        response['created_at'] = custom_datetime_format(response['created_at'])
        return response

class ActiveMobilePhoneSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ActiveMobilePhone
        exclude = ('category', 'location', 'scraping_url')
    
    def to_representation(self, instance):
        response = super().to_representation(instance) 
        response['product_model'] = instance.product_model.product_model.name if instance.product_model else ''
        response['brand'] = instance.brand.brand.name if instance.brand else ''
        response['color'] = instance.color.color.name if instance.color else ''
        response['storage'] = instance.storage.value if instance.storage else ''
        response['lock_status'] = instance.lock_status.name if instance.lock_status else ''
        response['condition'] = instance.condition.name if instance.condition else ''
        response['sold_price'] = f'${instance.sold_price}'
        response['shipping_fee'] = f'${instance.shipping_fee}'
        response['created_at'] = custom_datetime_format(response['created_at'])
        return response
