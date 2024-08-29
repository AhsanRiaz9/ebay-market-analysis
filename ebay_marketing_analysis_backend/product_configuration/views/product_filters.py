from rest_framework.views import APIView
from product_configuration.models import Condition, ConditionCategory, Category, ProductModelCategory
from product_configuration.serializers import ConditionSerializer, ColorCategorySerializer, BrandCategorySerializer, StorageSerializer, LockStatusSerializer, CategorySerializer, ProductModelCategorySerializer
from rest_framework.response import Response
from product_configuration.models import ColorCategory, BrandCategory, Storage, Condition, LockStatus, Category


class ProductFiltersView(APIView):

    def get(self, request, category_id, *args, **kwargs):
        category = Category.objects.filter(ebay_category_id=category_id).first()
        if category:
            mobile_phone_conditions = ConditionCategory.objects.filter(category=category)
            conditions = Condition.objects.filter(id__in=mobile_phone_conditions)
            colors = ColorCategory.objects.filter(category=category)
            brands = BrandCategory.objects.filter(category=category)
            storages = Storage.objects.all()
            lock_statuses = LockStatus.objects.all()
            product_models = ProductModelCategory.objects.filter(category=category).exclude(product_model=None)
            response = {
                'conditions': ConditionSerializer(conditions, many=True).data,
                'colors': ColorCategorySerializer(colors, many=True).data,
                'brands': BrandCategorySerializer(brands, many=True).data,
                'storages': StorageSerializer(storages, many=True).data,
                'lock_statuses': LockStatusSerializer(lock_statuses, many=True).data,
                'product_models': ProductModelCategorySerializer(product_models, many=True).data,
            }
            return Response(response)
        else:
            return Response({"message": "Category not found"}, status=404)

