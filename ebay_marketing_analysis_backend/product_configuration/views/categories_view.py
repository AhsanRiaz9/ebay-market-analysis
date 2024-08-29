from rest_framework.views import APIView
from product_configuration.models import Category
from product_configuration.serializers import CategorySerializer
from rest_framework.response import Response

class CategoriesView(APIView):

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)
