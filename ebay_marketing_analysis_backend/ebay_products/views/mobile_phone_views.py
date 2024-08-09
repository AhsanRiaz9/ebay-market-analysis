from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from ebay_products.serializers import MobilePhoneSerializer, ActiveMobilePhoneSerializer
from ebay_products.models import MobilePhone, ActiveMobilePhone
from ebay_products.utilis.paginations import MobilePhoneCustomPagination
from product_configuration.models import Condition

class MobilePhoneListView(APIView, MobilePhoneCustomPagination):
    
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
            if data_category == 'Active':
                queryset = queryset.filter(created_at__gte=start_date)
            else:
                queryset = queryset.filter(sold_date__gte=start_date)
            if len(date_range) == 2:
                end_date = date_range[1]
                if data_category == 'Active':
                    queryset = queryset.filter(created_at__lte=end_date)
                else:
                    queryset = queryset.filter(sold_date__lte=end_date)
        min_price = params.get('minPrice','')
        max_price = params.get('maxPrice','')
        if min_price:
            queryset = queryset.filter(sold_price__gte=min_price)
        if max_price:
            queryset = queryset.filter(sold_price__lte=max_price)
        conditions = params.get('conditions','')
        if conditions:
            conditions = conditions.split(',')
            queryset = queryset.filter(condition__ebay_condition_id__in=conditions)
        excluded_phrase = params.get('excludedPhrase','')
        if excluded_phrase:
            excluded_words = excluded_phrase.split(',')
            for excluded_word in excluded_words:
                queryset = queryset.exclude(title__icontains=excluded_word.lower().strip())
        colors = params.get('colors', '')
        if colors:
            colors = colors.split(',')
            queryset = queryset.filter(color__id__in=colors)
        brands = params.get('brands', '')
        if brands:
            brands = brands.split(',')
            queryset = queryset.filter(brand__id__in=brands)
        storages = params.get('storages', '')
        if storages:
            storages = storages.split(',')
            queryset = queryset.filter(storage__id__in=storages)
        lock_statuses = params.get('lock_statuses', '')
        if lock_statuses:
            lock_statuses = lock_statuses.split(',')
            queryset = queryset.filter(lock_status__id__in=lock_statuses)
        results = self.paginate_queryset(queryset, request, view=self)
        serializer = current_serializer(results, many=True)
        response = self.get_paginated_response(serializer.data, queryset)
        
        return response

