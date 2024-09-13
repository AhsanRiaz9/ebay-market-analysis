from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from competitor_analysis.models import EbayStore, StoreCategory
from settings.utilis.helpers import SeleniumWebDriver, extract_params_from_url
from rest_framework.status import HTTP_400_BAD_REQUEST
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from settings.utilis.formatters import format_info_value
import time
from product_configuration.models import Category

# Create your views here.
class DownloadEbayStoreView(APIView):
    permission_classes = (AllowAny,)
    
    def post(self, *args, **kwargs):
        url = 'https://www.ebay.com.au/str/originpc'
        params = self.request.data
        store_id = params.get('store_id', None)
        selenium_webdriver = None
        if store_id:
            selenium_webdriver = SeleniumWebDriver(headless=True)
            driver = selenium_webdriver.driver
            store_id = store_id.lower()
            ebay_store = self.download_ebay_store(driver, store_id)
            if ebay_store:
                self.download_store_categories(driver, ebay_store)
            response = {'data': 'Scraping of EbayStore started.'}
            status_code = 200
        else:
            response = {'error': 'Missing store_id.'}
            status_code = 400
        if selenium_webdriver:
            selenium_webdriver.close()
        return Response(response, status=status_code)
    
    def download_store_categories(self, driver, ebay_store):
        driver.get(ebay_store.url)
        time.sleep(2)
        category_btn = driver.find_elements(By.CSS_SELECTOR, 'div.str-controlbar__left-nav-btn')
        if category_btn:
            category_btn[0].click()
            see_more = driver.find_elements(By.CSS_SELECTOR, 'button.str-category-tree__toggle-show-more')
            if see_more:
                see_more[0].click()
                time.sleep(2)
            store_categories = driver.find_elements(By.CSS_SELECTOR, 'ul.str-category-tree__list>li a')
            if store_categories:
                category_param = None
                for store_category in store_categories:
                    category_name = store_category.text
                    category_url = store_category.get_attribute('href')
                    params = extract_params_from_url(category_url)
                    if not category_param:
                        if '_sacat' in params:
                            category_param = '_sacat'
                        else:
                            category_param = 'store_cat'
                    category_id = params.get(category_param)
                    # print(category_param, category_id)
                    # print(f'Category: {category_name}, URL: {category_url}')
                    self.save_ebay_store_category(ebay_store, category_id, category_name)
                if category_param:
                    ebay_store.category_param = category_param
                    ebay_store.save()
        print('Ebay Store Categories saved successfully.')
    
    def save_ebay_store_category(self, ebay_store, category_id, category_name):
        category_id = int(category_id)
        category = Category.objects.filter(ebay_category_id=category_id).first()
        if not category:
            category = Category.objects.create(name=category_name, ebay_category_id=category_id)
        store_category = StoreCategory.objects.filter(ebay_store=ebay_store, category=category).first()
        if not store_category:
            store_category = StoreCategory.objects.create(ebay_store=ebay_store, category=category)
            # print('Store Category saved successfully.')
            
    def download_ebay_store(self, driver, store_id):
        ebay_store = None
        try:
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
                view_all_btn = driver.find_elements(By.CSS_SELECTOR, '.str-marginals__footer>a')
                if view_all_btn:
                    store_url = view_all_btn[0].get_attribute('href')
                    params = extract_params_from_url(store_url)
                    ebay_store = EbayStore.objects.filter(ebay_store_id=store_id).first()
                    if not ebay_store:
                        ebay_store = EbayStore.objects.create(name=store_name, feedback=feedback, items_sold=items_sold, url=store_link, ebay_store_id=store_id, followers=followers, ssn_code=params.get('_ssn', ''))
                    else:
                        ebay_store.feedback = feedback
                        ebay_store.items_sold = items_sold
                        ebay_store.url = store_link
                        ebay_store.followers = followers
                        ebay_store.ssn_code = params.get('_ssn', '')
                        ebay_store.save()
        except Exception as e:
            print(e)
            ebay_store = None
        finally:
            return ebay_store