from rest_framework.generics import ListAPIView
from ebay_products.serializers import MobilePhoneSerializer
from ebay_products.models import MobilePhone
from ebay_products.utilis.paginations import CutstomPagination

class MobilePhoneListView(ListAPIView):
    model = MobilePhone
    serializer_class = MobilePhoneSerializer
    queryset = MobilePhone.objects.all().order_by('-created_at')
    pagination_class = CutstomPagination
    
    
    

