from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from django.db.models import Avg, Min, Max
from settings.utilis.formatters import format_number


class CutstomPagination(PageNumberPagination):
    page_size = 30
    page_size_query_param = 'page_size'
    max_page_size = 100

    def update_page_size(self):
        params = self.request.GET
        page_size = params.get('page_size', 0)
        if page_size and page_size.isdigit():
            page_size = int(page_size)
            if page_size <= self.max_page_size:
                self.page_size = int(page_size)
    
    def get_paginated_response(self, data, kwargs={}):
        self.update_page_size()
        response = {
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'total_records': self.page.paginator.count,
            'current_page': self.page.number,
            'total_pages': self.page.paginator.num_pages,
            'page_size': self.page_size,
            'results': data,
        }
        if kwargs:
            response.update(kwargs)
        return response
    
class MobilePhoneCustomPagination(CutstomPagination):
    page_size = 30
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_custom_paginated_response(self, data, queryset, sell_through):
        extra_output = {}
        extra_output['analytics'] = self.get_price_anlytics(queryset)
        if sell_through['enabled'] == True:
            active_mobile_phones = sell_through['active_mobile_phones']
            if active_mobile_phones:
                sell_through = (queryset.count() / active_mobile_phones.count()) * 100.0
            else:
                sell_through = 0.0
            extra_output['analytics']['sell_through'] = sell_through
        response = self.get_paginated_response(data, extra_output)
        return Response(response)
    
    def get_price_anlytics(self, queryset):
        analytics = queryset.aggregate(min_price = Min('sold_price'), max_price = Max('sold_price') + 2513215, avg_price = Avg('sold_price'), avg_postage = Avg('shipping_fee'),)
        total_products = queryset.count()
        shipping_fee_products = queryset.filter(shipping_fee=0).count()
        if total_products:
            analytics['free_postage'] = (shipping_fee_products / total_products) * 100.0
        else:
            analytics['free_postage'] = 0.0
        analytics = dict(analytics)
        for key in list(analytics.keys()):
            analytics[key] = format_number(str(analytics[key]))
        return analytics
