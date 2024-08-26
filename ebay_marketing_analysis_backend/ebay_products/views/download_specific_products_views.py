import os
import time
from rest_framework import status
from rest_framework.views import APIView
import threading
from rest_framework.response import Response

class DownloadSpecificProductsView(APIView):
    def post(self, request, *args, **kwargs):
        scraping_url = request.data.get('scraping_url', '')
        if scraping_url:
            scraping_thread = threading.Thread(target=self.scrap_products, args=[scraping_url,], daemon=True)
            scraping_thread.start()
            return Response({'message': f'Background job started to download specific product against url: {scraping_url}'})
        else:
            return Response({'detail': 'Scraping URL not provided'}, status=status.HTTP_400_BAD_REQUEST)
    
    def scrap_products(self, scraping_url):
        print(scraping_url)
        pass
