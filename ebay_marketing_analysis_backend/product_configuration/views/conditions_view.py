from rest_framework.generics import ListAPIView
from product_configuration.models import Condition, ConditionCategory, Category
from ebay_products.utilis.paginations import CutstomPagination
from product_configuration.serializers import ConditionSerializer

class ConditionListView(ListAPIView):
    model = Condition
    serializer_class = ConditionSerializer
    pagination_class = None

    def get_queryset(self):
        category = Category.objects.filter(ebay_category_id=9355).first()
        mobile_phone_conditions = ConditionCategory.objects.filter(category=category).values_list('id')
        queryset = Condition.objects.filter(id__in=mobile_phone_conditions)
        return queryset
