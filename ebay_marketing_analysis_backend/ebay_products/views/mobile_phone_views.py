from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from ebay_products.serializers import MobilePhoneSerializer, ActiveMobilePhoneSerializer
from ebay_products.models import MobilePhone, ActiveMobilePhone
from ebay_products.utilis.paginations import CutstomPagination
from product_configuration.models import Condition

class MobilePhoneListView(APIView, CutstomPagination):
    
    def get(self, request, *args, **kwargs):
        params = self.request.GET
        data_category = params.get('dataCategory', 'Active')
        if data_category == 'Active':
            Model = ActiveMobilePhone
            current_serializer = ActiveMobilePhoneSerializer
        else:
            Model = MobilePhone
            current_serializer = MobilePhoneSerializer
        queryset = Model.objects.all().order_by('-created_at')
        title = params.get('title', '').lower().strip()
        if title:
            queryset = queryset.filter(title__icontains=title)
        date_range = params.get('date_range','')
        if date_range:
            date_range = date_range.split(' to ')
            start_date = date_range[0]
            queryset = queryset.filter(sold_date__gte=start_date)
            if len(date_range) == 2:
                end_date = date_range[1]
                queryset = queryset.filter(sold_date__lte=end_date)
        min_price = params.get('minPrice','')
        max_price = params.get('maxPrice','')
        if min_price:
            queryset = queryset.filter(sold_price__gte=min_price)
        if max_price:
            queryset = queryset.filter(sold_price__lte=max_price)
        condition = params.get('condition','')
        if condition:
            condition = Condition.objects.filter(ebay_condition_id=condition).first()
            queryset = queryset.filter(condition=condition)
        excluded_phrase = params.get('excludedPhrase','')
        if excluded_phrase:
            excluded_words = excluded_phrase.split(',')
            for excluded_word in excluded_words:
                queryset = queryset.exclude(title__icontains=excluded_word.lower().strip())
        results = self.paginate_queryset(queryset, request, view=self)
        serializer = current_serializer(results, many=True)
        return self.get_paginated_response(serializer.data)
        

