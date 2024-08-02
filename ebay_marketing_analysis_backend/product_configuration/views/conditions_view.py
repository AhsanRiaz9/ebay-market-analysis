from rest_framework.generics import ListAPIView
from product_configuration.models import Condition
from ebay_products.utilis.paginations import CutstomPagination
from product_configuration.serializers import ConditionSerializer

class ConditionListView(ListAPIView):
    model = Condition
    queryset = Condition.objects.all().order_by('pk')
    serializer_class = ConditionSerializer

