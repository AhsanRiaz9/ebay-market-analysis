from rest_framework.views import APIView
from product_configuration.models import Condition, ConditionCategory, Category
from ebay_products.utilis.paginations import CutstomPagination
from product_configuration.serializers import ConditionSerializer, ColorCategorySerializer, BrandCategorySerializer, StorageSerializer, LockStatusSerializer
from rest_framework.response import Response
from product_configuration.models import ColorCategory, BrandCategory, Storage, Condition, ProductModelCategory, LockStatus, Category


class ProductFiltersView(APIView):

    def get(self, request, *args, **kwargs):
        category_id = 9355
        category = Category.objects.filter(ebay_category_id=category_id).first()
        mobile_phone_conditions = ConditionCategory.objects.filter(category=category)
        conditions = Condition.objects.filter(id__in=mobile_phone_conditions)
        colors = ColorCategory.objects.filter(category=category)
        brands = BrandCategory.objects.filter(category=category)
        storages = Storage.objects.all()
        lock_statuses = LockStatus.objects.all()
        response = {
            'conditions': ConditionSerializer(conditions, many=True).data,
            'colors': ColorCategorySerializer(colors, many=True).data,
            'brands': BrandCategorySerializer(brands, many=True).data,
            'storages': StorageSerializer(storages, many=True).data,
            'lock_statuses': LockStatusSerializer(lock_statuses, many=True).data
        }
        return Response(response)


