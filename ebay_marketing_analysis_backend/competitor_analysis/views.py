from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from competitor_analysis.models import EbayStore
from settings.utilis.helpers import SeleniumWebDriver
from rest_framework.status import HTTP_400_BAD_REQUEST
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from settings.utilis.formatters import format_info_value


# Create your views here.
class DownloadEbayStoreView(APIView):
    permission_classes = (AllowAny,)
    
    def post(self, *args, **kwargs):
        url = 'https://www.ebay.com.au/str/originpc'
        params = self.request.data
        store_id = params.get('store_id', None)
        if store_id:
            store_id = store_id.lower()
            ebay_store = self.download_ebay_store(store_id)
            print(ebay_store)
            return Response({'data': 'Scraping of EbayStore started.'})
        else:
            return Response({'error': 'Missing store_id.'}, status=400)
    
    def download_ebay_store(self, store_id):
        selenium_webdriver = None
        try:
            ebay_store = EbayStore.objects.filter(ebay_store_id=store_id).first()
            if not ebay_store:
                selenium_webdriver = SeleniumWebDriver(headless=True)
                driver = selenium_webdriver.driver
                url = f'https://www.ebay.com.au/str/{store_id}'
                driver.get(url)
                store_div = driver.find_elements(By.CSS_SELECTOR, 'div.str-seller-card')
                if store_div:
                    store_div = store_div[0]
                    store_name_element = store_div.find_element(By.CSS_SELECTOR, 'h1>a')
                    store_name = store_name_element.text
                    store_link = store_name_element.get_attribute('href')
                    store_details = store_div.find_elements(By.CSS_SELECTOR, '.str-seller-card__store-stats-content > div')
                    items_sold = 0
                    followers = 0
                    for store_detail in store_details:
                        store_detail = store_detail.text.lower()
                        if '%' in store_detail:
                            feedback = store_detail.split('%')[0]
                        elif 'items sold' in store_detail:
                            items_sold = store_detail.split(' ')[0]
                            items_sold = format_info_value(items_sold)
                        elif 'followers' in store_detail:
                            followers = store_detail.split(' ')[0]
                            followers = format_info_value(followers)
                    ebay_store = EbayStore.objects.create(name=store_name, feedback=feedback, items_sold=items_sold, url=store_link, ebay_store_id=store_id, followers=followers)
        except Exception as e:
            print(e)
            if selenium_webdriver:
                selenium_webdriver.close()
            ebay_store = None
        finally:
            if selenium_webdriver:
                selenium_webdriver.close()
            return ebay_store