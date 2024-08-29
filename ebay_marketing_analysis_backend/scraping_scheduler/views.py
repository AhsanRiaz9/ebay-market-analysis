from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from scraping_scheduler.models import SpecificProductProcess
from scraping_scheduler.serializers import SpecificProductProcessSerializer
from rest_framework.response import Response
from ebay_products.utilis.paginations import CutstomPagination

class SpecificProductsProcessView(ListAPIView):
    permission_classes = (IsAuthenticated, )
    queryset = SpecificProductProcess.objects.all()
    serializer_class = SpecificProductProcessSerializer
    pagination_class = CutstomPagination
