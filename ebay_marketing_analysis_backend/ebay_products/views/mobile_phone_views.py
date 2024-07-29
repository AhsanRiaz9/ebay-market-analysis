from rest_framework.generics import ListAPIView
from ebay_products.serializers import MobilePhoneSerializer
from ebay_products.models import MobilePhone
from ebay_products.utilis.paginations import CutstomPagination

class MobilePhoneListView(ListAPIView):
    model = MobilePhone
    serializer_class = MobilePhoneSerializer
    pagination_class = CutstomPagination
    

    def get_queryset(self):
        queryset = MobilePhone.objects.all().order_by('-created_at')
        params = self.request.GET
        title = params.get('title', '')
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
        return queryset
