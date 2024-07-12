from rest_framework.views import APIView
from rest_framework.response import Response
from settings.utilis.helpers import SeleniumWebDriver, create_encoded_url, format_date
from product_configuration.models import ProductModel, BrandCategory, ColorCategory, Category, Storage, ProductModelCategory, Condition, ConditionCategory, LockStatus, Location, Brand, Color
from ebay_products.models import MobilePhones
import threading
import copy
from tqdm import tqdm
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup
from selenium.common.exceptions import InvalidArgumentException

# Create your views here.
class DownloadProduct(APIView):
    def get(self, request, category_id, *args, **kwargs):    
        t = threading.Thread(target=self.download_data, args=[category_id,],daemon=True)
        t.start()
        return Response({'message': f'Background job started to download product data of category {category_id}.'})
    
    def download_data(self, category_id):
        try:
            url = f'https://www.ebay.com.au/b/{category_id}/'
            category = Category.objects.filter(ebay_category_id=category_id).first()
            if not category:
                raise Exception('No category available.')
            conditions = ConditionCategory.objects.filter(category=category)
            for condition_category in conditions:
                self.download_mobile_data(url, condition_category.condition, category_id)
        except Exception as e:
            print(e)
        return Response({'message': 'Download product successfully.'})

    def items_exists(self, encoded_url, attempt=0):
        driver = self.selenium_webdriver.driver
        try:
            items = driver.find_elements(By.CSS_SELECTOR, 'li.s-item')
            return len(items) > 0
        except Exception as e:
            self.selenium_webdriver.close()
            self.selenium_webdriver = SeleniumWebDriver(headless=False)
            self.selenium_webdriver.driver.get(encoded_url)
            time.sleep(3)
            if attempt == 0:
                return self.items_exists(encoded_url, attempt+1)
            else:
                return False
    
    def custom_tab_info(self, encoded_url, tab_name, attempt=0):
        driver = self.selenium_webdriver.driver
        try:
            filter_values = []
            self._open_filters(driver)
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div[role="tab"]'))
            )
            filter_tabs = driver.find_elements(By.CSS_SELECTOR, 'div[role="tab"]')
            custom_tab = [tab for tab in filter_tabs if tab.text==tab_name]
            if custom_tab:
                custom_tab[0].click()
                time.sleep(3)
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'div.x-overlay__wrapper--right'))
                )
                tab_info = driver.find_element(By.CSS_SELECTOR, 'div.x-overlay__wrapper--right')
                tab_info = tab_info.get_attribute('innerHTML')
                soup = BeautifulSoup(tab_info)
                excluded_values = ('Not Specified', 'All listings', 'Best Offer')
                filter_values = [label.text for label in soup.select('label.field__label > span') if label.text not in excluded_values ]
                print(filter_values)
            self._close_filters(driver)
            return filter_values
        except Exception as e:
            if attempt == 0:
                self.selenium_webdriver.close()
                self.selenium_webdriver = SeleniumWebDriver(headless=False)
                self.selenium_webdriver.driver.get(encoded_url)
                time.sleep(3)
                return self.custom_tab_info(encoded_url, tab_name, attempt+1)
            else:
                return []
        
    def _open_filters(self, driver):
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "button[aria-label='All filters']"))
            )
            filter_all_btn = driver.find_elements(By.CSS_SELECTOR, "button[aria-label='All filters']")
            if filter_all_btn:
                filter_all_btn[0].click()
                return True
        except Exception as e:
            print(e)
        return False
    
    def _close_filters(self, driver):
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '.x-overlay__container>button'))
            )
            overlay_close = driver.find_elements(By.CSS_SELECTOR, '.x-overlay__container>button')
            if overlay_close:
                overlay_close[0].click()
                time.sleep(2)
                return True
        except Exception as e:
            print(e)
        return False
    
    def download_mobile_data(self, url, condition, category_id):
        self.selenium_webdriver = SeleniumWebDriver(headless=False)
        self.visit_count = 0
        params = {
            'LH_Complete': 1, 
            'LH_Sold': 1,
            'rt': 'nc', 
            'LH_BIN': 1,
            'mag': 1,
            'LH_ItemCondition': condition.ebay_condition_id,
            '_sop': 10
        }
        encoded_url = create_encoded_url(url, params)
        self.visit_url(encoded_url)
        mobile_phones = self.custom_tab_info(encoded_url, 'Model')
        for mobile in tqdm(mobile_phones):
            try:
                filter_params = copy.deepcopy(params)
                filter_params.update({'Model': mobile})
                encoded_url = create_encoded_url(url, filter_params)
                self.visit_url(encoded_url)
                if self.items_exists(encoded_url) == False:        
                    continue
                brands_data = self.custom_tab_info(encoded_url, 'Brand')
                if not brands_data:
                    brands_data = ['']
                for brand_name in brands_data:
                    filter_params = copy.deepcopy(params)
                    filter_params.update({'Model': mobile, 'Brand': brand_name})
                    encoded_url = create_encoded_url(url, filter_params)
                    self.visit_url(encoded_url)
                    if self.items_exists(encoded_url) == False:        
                        continue
                    storage_data = self.custom_tab_info(encoded_url, 'Storage Capacity')
                    if not storage_data:
                        storage_data = ['']
                    for storage in storage_data:
                        filter_params = copy.deepcopy(params)
                        filter_params.update({'Model': mobile, 'Brand': brand_name, 'Storage Capacity': storage})
                        encoded_url = create_encoded_url(url, filter_params)
                        self.visit_url(encoded_url)
                        time.sleep(2)
                        if self.items_exists(encoded_url) == False:        
                            continue
                        colors_data = self.custom_tab_info(encoded_url, 'Colour')
                        if not colors_data:
                            colors_data = ['']
                        for color in colors_data:
                            filter_params = copy.deepcopy(params)
                            filter_params.update({'Model': mobile, 'Brand': brand_name, 'Storage Capacity': storage, 'Colour': color})
                            encoded_url = create_encoded_url(url, filter_params)
                            self.visit_url(encoded_url)
                            time.sleep(2)
                            if self.items_exists(encoded_url) == False:        
                                continue
                            lock_statues_data = self.custom_tab_info(encoded_url, 'Lock Status')
                            if not lock_statues_data:
                                lock_statues_data = ['']
                            for lock_status in lock_statues_data:
                                filter_params = copy.deepcopy(params)
                                filter_params.update({'Model': mobile, 'Brand': brand_name, 'Storage Capacity': storage, 'Colour': color, 'Lock Status': lock_status})
                                encoded_url = create_encoded_url(url, filter_params)
                                self.visit_url(encoded_url)
                                time.sleep(2)
                                if self.items_exists(encoded_url) == False:
                                    continue
                                self.scrap_data(url, params, {'Model': mobile, 'Brand': brand_name, 'Storage Capacity': storage, 'Colour': color, 'Lock Status': lock_status}, category_id)
            except Exception as e:
                print('Error occur in mobile loop', e, encoded_url)
                continue
            
        self.selenium_webdriver.close()
    
    def visit_url(self, url):
        try:
            self.visit_count += 1
            close_browser = self.visit_count%20==0
            if not close_browser:
                self.selenium_webdriver.driver.get(url)
                time.sleep(3)
            body_text = self.selenium_webdriver.driver.find_element(By.CSS_SELECTOR, 'body').text
            error_msg = 'An error occurred while processing your request.'
            if self.visit_count%20==0 or error_msg in body_text:
                self.selenium_webdriver.close()
                self.selenium_webdriver = SeleniumWebDriver(headless=False)
                self.selenium_webdriver.driver.get(url)
                time.sleep(3)
        except InvalidArgumentException as e:
            self.selenium_webdriver.close()
            self.selenium_webdriver = SeleniumWebDriver(headless=False)
            self.selenium_webdriver.driver.get(url)
        except Exception as e:
            print('Error occur in visit url, exception =>', e)
         
    def scrap_data(self, url, params, filter_conditions, category_id):
        driver = self.selenium_webdriver.driver
        location = Location.objects.filter(domain='ebay.com.au').first()
        filter_params = copy.deepcopy(params)
        filter_params.update(filter_conditions)
        encoded_url = create_encoded_url(url, filter_params)
        self.visit_url(encoded_url)
        time.sleep(3)
        mobile_phones_objects = []
        print(filter_params)
        data_available = True
        while data_available:
            try:
                print('data available', data_available)
                items = driver.find_elements(By.CSS_SELECTOR, 'li.s-item')
                if len(items) == 0:
                    data_available = False
                for item in tqdm(items):
                    item.location_once_scrolled_into_view
                    title = item.find_element(By.CSS_SELECTOR, 'h3').text
                    image = item.find_element(By.CSS_SELECTOR, 'img').get_attribute('src')
                    sold_price = item.find_elements(By.CSS_SELECTOR, 'span.s-item__price')
                    if not sold_price:
                        sold_price = item.find_elements(By.CSS_SELECTOR, 'span.bsig__price')
                    sold_price = sold_price[0].text.split('-')[0].replace('AU $', '').strip()
                    if ' to ':
                        sold_price = sold_price.split(' to ')[0]
                    sold_price = float(sold_price)
                    product_url = item.find_elements(By.CSS_SELECTOR, 'div.s-item__info > a')
                    if not product_url:
                        product_url = item.find_elements(By.CSS_SELECTOR, 'span.bsig__title > a')
                    product_url = product_url[0].get_attribute('href')
                    if 'itm' in product_url:
                        ebay_item_id = int(product_url.split('?')[0].split('itm/')[1])    
                    else:
                        ebay_item_id = int(product_url.split('?')[0].split('p/')[1])
                    product_url = product_url.split('?')[0]    
                    sold_date = item.find_elements(By.CSS_SELECTOR, 'span.s-item__pl > span > span')
                    if sold_date:
                        sold_date = sold_date[0].get_attribute('data-w')
                        sold_date = format_date(sold_date)
                    else:
                        sold_date = ''
                    shipping_fee = item.find_elements(By.CSS_SELECTOR, 'span.s-item__shipping')
                    if not shipping_fee:
                        shipping_fee = item.find_elements(By.CSS_SELECTOR, 'span.bsig__logisticsCost')
                    if shipping_fee:
                        shipping_fee = shipping_fee[0].text
                        if shipping_fee.lower() == 'free':
                            shipping_fee = 0.0
                        else:
                            shipping_fee = shipping_fee.split(' postage')[0].replace('AU $', '').strip()
                            shipping_fee = float(shipping_fee)
                    product_model = ProductModelCategory.objects.filter(product_model__name=filter_conditions['Model']).first()
                    if not product_model:
                        product_model = self.create_product_model(filter_conditions['Model'], category_id)
                    brand = BrandCategory.objects.filter(brand__name=filter_conditions['Brand']).first()
                    if not brand:
                        brand = self.create_brand(filter_conditions['Brand'], category_id)
                    color = ColorCategory.objects.filter(color__name=filter_conditions['Colour']).first()
                    if not color:
                        color = self.create_color(filter_conditions['Colour'], category_id)
                    storage = Storage.objects.filter(value=filter_conditions['Storage Capacity']).first()
                    if not storage:
                        storage = self.create_storage(filter_conditions['Storage Capacity'])
                    condition = Condition.objects.filter(ebay_condition_id=params['LH_ItemCondition']).first()
                    lock_status = LockStatus.objects.filter(name=filter_conditions['Lock Status']).first()
                    if not lock_status:
                        lock_status = self.create_lock_status(filter_conditions['Lock Status'])
                    category = Category.objects.filter(ebay_category_id=category_id).first()
                    mobile_phone = MobilePhones(title=title, sold_price=sold_price, shipping_fee=shipping_fee, ebay_item_id=ebay_item_id,
                       product_url=product_url, image=image, category=category, product_model=product_model, brand=brand, color=color, storage=storage, lock_status=lock_status,
                       location=location, condition=condition, sold_date=sold_date)
                    mobile_phones_objects.append(mobile_phone)
                next_btn = driver.find_elements(By.CSS_SELECTOR, 'a.pagination__next')
                if next_btn:
                    driver.get(next_btn[0].get_attribute('href'))
                else:
                    data_available = False
                time.sleep(3)
                print(mobile_phones_objects)
            except Exception as e:
                print(e)
                data_available = False
                break 
        if mobile_phones_objects:
            MobilePhones.objects.bulk_create(mobile_phones_objects, ignore_conflicts=True, batch_size=100)    
    
    def create_product_model(self, model_name, category_id):
        product_model_category = None
        if model_name:
            prodcut_model = ProductModel.objects.create(name=model_name)
            product_model_category = ProductModelCategory(product_model=prodcut_model, category__ebay_category_id=category_id)
        return product_model_category
    
    def create_brand(self, brand_name, category_id):
        brand_category = None
        if brand_name:
            brand = Brand.objects.create(name=brand_name)
            brand_category = BrandCategory.objects.create(brand=brand, category__ebay_category_id=category_id)
        return brand_category
    
    def create_color(self, color_name, category_id):
        color_category = None
        if color_name:
            color = Color.objects.create(name=color_name)
            color_category = ColorCategory.objects.create(color=color, category__ebay_category_id=category_id)
        return color_category
    
    def create_storage(self, storage_value):
        storage = None
        if storage_value:
            storage = Storage.objects.create(value=storage_value)
        return storage
    
    def create_lock_status(self, lock_status_value):
        lock_status = None
        if lock_status_value:
            lock_status = LockStatus.objects.create(name=lock_status_value)
        return lock_status