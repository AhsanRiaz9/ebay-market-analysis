from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from scraping_scheduler.models import SpecificProductProcess
from scraping_scheduler.serializers import SpecificProductProcessSerializer
from rest_framework.response import Response

class SpecificProductsProcessView(APIView):
    permission_classes = (AllowAny, )
    
    def get(self, request, *args, **kwargs):
        objects = SpecificProductProcess.objects.all()
        serializer = SpecificProductProcessSerializer(objects, many=True)
        return Response(serializer.data)
