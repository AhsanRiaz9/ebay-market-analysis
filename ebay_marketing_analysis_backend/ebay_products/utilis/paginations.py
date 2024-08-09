from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from django.db.models import Avg, Min, Max

class CutstomPagination(PageNumberPagination):
    page_size = 30
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'total_records': self.page.paginator.count,
            'current_page': self.page.number,
            'total_pages': self.page.paginator.num_pages,
            'page_size': self.page_size,
            'results': data
        })
    
class MobilePhoneCustomPagination(PageNumberPagination):
    page_size = 30
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data, queryset):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'total_records': self.page.paginator.count,
            'current_page': self.page.number,
            'total_pages': self.page.paginator.num_pages,
            'page_size': self.page_size,
            'analytics': self.get_price_anlytics(queryset),
            'results': data
        })
    
    def get_price_anlytics(self, queryset):
        analytics = queryset.aggregate(min_price = Min('sold_price'), max_price = Max('sold_price'), avg_price = Avg('sold_price'), avg_postage = Avg('shipping_fee'),)
        total_products = queryset.count()
        shipping_fee_products = queryset.filter(shipping_fee=0).count()
        if total_products:
            analytics['free_postage'] = (shipping_fee_products / total_products) * 100.0
        else:
            analytics['free_postage'] = 0.0
        return analytics
