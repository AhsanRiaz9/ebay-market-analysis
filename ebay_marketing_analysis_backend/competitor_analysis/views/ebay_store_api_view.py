from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from competitor_analysis.models import EbayStore, StoreCategory, EbayStoreProduct
from rest_framework.status import HTTP_400_BAD_REQUEST
from settings.utilis.formatters import format_info_value
import time
from product_configuration.models import Category
from tqdm import tqdm
from settings.utilis.formatters import format_price
from settings.utilis.ebay_apis import EbayOAuthService, EbayAPIService
import requests
from dotenv import load_dotenv
import os
load_dotenv('.env')

# Create your views here.
class DownloadEbayStoreAPIView(APIView):
    permission_classes = (AllowAny,)
    
    def post(self, *args, **kwargs):
        client_id = os.environ.get('CLIENT_ID')
        client_secret = os.environ.get('CLIENT_SECRET')
        redirect_uri = os.environ.get('REDIRECT_URI')
        scope = os.environ.get('SCOPE')
        ebay_api_service = EbayAPIService(client_id, client_secret, redirect_uri, scope)
        params = self.request.data
        store_id = params.get('store_id', None)
        if store_id:
            store_id = store_id.lower()
            ebay_store = EbayStore.objects.filter(ebay_store_id=store_id).first()
            if not ebay_store:
                ebay_store = self.create_ebay_store(store_id)
            store_data = ebay_api_service.fetch_ebay_store(store_id)
            self.save_ebay_store_data(ebay_store, store_data)
            response = {'data': 'Scraping of EbayStore started.'}
            status_code = 200
        else:
            response = {'error': 'Missing store_id.'}
            status_code = 400
        return Response(response, status=status_code)
        
    def create_ebay_store(self, store_id):
        url = f'https://www.ebay.com.au/str/{store_id}'
        ebay_store = EbayStore.objects.create(ebay_store_id=store_id, url=url)
        return ebay_store
    
    def save_ebay_store_data(self, ebay_store, store_data):
        products = store_data['products']
        import pdb
        pdb.set_trace()
        print(len(products))