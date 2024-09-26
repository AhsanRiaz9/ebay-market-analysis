from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from competitor_analysis.models import EbayStore, StoreCategory, EbayStoreProduct
from settings.utilis.helpers import SeleniumWebDriver, extract_params_from_url, format_date
from rest_framework.status import HTTP_400_BAD_REQUEST
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from settings.utilis.formatters import format_info_value
import time
from product_configuration.models import Category
from tqdm import tqdm
from settings.utilis.formatters import format_price

# Create your views here.
class DownloadEbayStoreView(APIView):
    permission_classes = (AllowAny,)
    
    def post(self, *args, **kwargs):
        params = self.request.data
        store_id = params.get('store_id', None)
        selenium_webdriver = None
        if store_id:
            selenium_webdriver = SeleniumWebDriver(headless=False)
            driver = selenium_webdriver.driver
            store_id = store_id.lower()
            ebay_store = self.download_ebay_store(driver, store_id)
            if ebay_store:
                self.download_store_categories(driver, ebay_store)
                self.download_store_products(driver, ebay_store)
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
            import pdb
            pdb.set_trace()
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
        
    def download_store_products(self, driver, ebay_store):
        store_categories = StoreCategory.objects.filter(ebay_store=ebay_store)
        listing_types = ['sold', 'active']
        for listing_type in listing_types:
            sold_listing = True if listing_type == 'sold' else False
            for store_category in tqdm(store_categories):
                category_id = store_category.category.ebay_category_id
                url = f'https://www.ebay.com.au/sch/i.html?_dkr=1&iconV2Request=true&_blrs=recall_filtering&_ssn={ebay_store.ssn_code}&{ebay_store.category_param}={category_id}&store_name={ebay_store.ebay_store_id}&_oac=1&&_dmd=1&_ipg=240'
                if listing_type == 'sold':
                    url += '&LH_Sold=1&LH_Complete=1'
                print(url)
                driver.get(url)
                pagination_end = False
                while pagination_end != True:
                    try:
                        time.sleep(2)
                        product_elements = driver.find_elements(By.CSS_SELECTOR, 'ul.srp-results div.s-item__wrapper')
                        ebay_products = []
                        for product_element in product_elements:
                            product_element.location_once_scrolled_into_view
                            product_title = product_element.find_element(By.CSS_SELECTOR, 'div.s-item__title').text
                            product_price = product_element.find_element(By.CSS_SELECTOR, 'span.s-item__price').text
                            product_price = format_price(product_price)
                            postage_price = product_element.find_element(By.CSS_SELECTOR, 'span.s-item__shipping').text
                            postage_price = format_price(postage_price)
                            product_url = product_element.find_element(By.TAG_NAME, 'a').get_attribute('href')
                            product_url_params = [url_params for url_params in product_url.split('?')[1].split('&') if 'itmmeta' not in url_params]
                            product_url = f"{product_url.split('?')[0]}?{'&'.join(product_url_params)}"
                            image = product_element.find_element(By.TAG_NAME, 'img').get_attribute('src')
                            if 'itm' in product_url:
                                ebay_item_id = int(product_url.split('?')[0].split('itm/')[1])    
                            else:
                                ebay_item_id = int(product_url.split('?')[0].split('p/')[1])
                            sold_date = None
                            if sold_listing == True:
                                sold_date = product_element.find_elements(By.CSS_SELECTOR, 'span.s-item__caption--signal')
                                if sold_date:
                                    sold_date = sold_date[0].text
                                    sold_date = format_date(sold_date)
                                    print(sold_date)
                            ebay_store_product = EbayStoreProduct.objects.filter(title=product_title, ebay_store=ebay_store, product_url=product_url, ebay_item_id=ebay_item_id, sold_date=sold_date, is_sold_listing=sold_listing).first()
                            if not ebay_store_product:
                                ebay_product = EbayStoreProduct(title=product_title, price=product_price, shipping_fee=postage_price, ebay_item_id=ebay_item_id, product_url=product_url, image=image, category=store_category.category, ebay_store=ebay_store, sold_date=sold_date, is_sold_listing=sold_listing)
                                ebay_products.append(ebay_product)
                        next_btn = driver.find_elements(By.CSS_SELECTOR, 'a.pagination__next')
                        if next_btn:
                            next_btn[0].click()
                            time.sleep(3)
                        else:
                            pagination_end = True
                        print('Saving products to database ...')
                        EbayStoreProduct.objects.bulk_create(ebay_products, ignore_conflicts=True, batch_size=50)
                    except Exception as e:
                        print(e)
                        pagination_end = True
