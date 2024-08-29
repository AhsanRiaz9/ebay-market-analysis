from rest_framework.views import APIView
from ebay_products.serializers import MobilePhoneSerializer, ActiveMobilePhoneSerializer
from ebay_products.models import MobilePhone, ActiveMobilePhone
from ebay_products.utilis.paginations import MobilePhoneCustomPagination
from rest_framework.permissions import IsAuthenticated
from product_configuration.models import Category

class MobilePhoneListView(APIView, MobilePhoneCustomPagination):
    
    permission_classes = (IsAuthenticated, )
    
    def get(self, request, *args, **kwargs):
        params = self.request.GET
        data_category = params.get('dataCategory', 'Active')
        sell_through = {'enabled' : False}
        if data_category == 'Active':
            queryset = self.filter_mobile_phones(params, data_category, ActiveMobilePhone)
            current_serializer = ActiveMobilePhoneSerializer
        else:
            queryset = self.filter_mobile_phones(params, data_category, MobilePhone)
            active_mobile_phones = self.filter_mobile_phones(params, 'Active', ActiveMobilePhone)
            current_serializer = MobilePhoneSerializer
            sell_through['enabled'] = True
            sell_through['active_mobile_phones'] = active_mobile_phones
        results = self.paginate_queryset(queryset, request, view=self)
        serializer = current_serializer(results, many=True)
        response = self.get_custom_paginated_response(serializer.data, queryset, sell_through)
        return response


    def filter_mobile_phones(self, params, data_category, Model):
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
            if len(date_range) == 2 and start_date != date_range[1]:
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
        category_id = params.get('category', '')
        if category_id:
            category = Category.objects.filter(ebay_category_id=category_id).first()
            queryset = queryset.filter(category=category)
        product_models = params.get('product_models', '')
        if product_models:
            product_models = product_models.split(',')
            queryset = queryset.filter(id__in=product_models)
        return queryset