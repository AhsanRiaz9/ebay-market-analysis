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
            queryset = queryset.filter(condition__ebay_condition_id=condition)
        excluded_phrase = params.get('excludedPhrase','')
        if excluded_phrase:
            excluded_words = excluded_phrase.split(',')
            for excluded_word in excluded_words:
                queryset = queryset.exclude(title__icontains=excluded_word.lower().strip())
        return queryset

