from settings.utilis.helpers import SeleniumWebDriver, create_encoded_url, decode_string,  format_date, check_internet_connection, create_internet_connection, check_webdriver_close_exception, refresh_ip
from product_configuration.models import BrandCategory, ColorCategory, Category, Storage, ProductModel, ProductModelCategory, Condition, ConditionCategory, LockStatus, Location, Brand, Color, EbayDomain
from ebay_products.models import MobilePhone, ActiveMobilePhone
from tqdm import tqdm
from selenium.webdriver.common.by import By
import time
from settings.utilis.helpers import decode_string

class SpecificProductScraper:
    def scrap_products(self, scraping_url, is_sold_listing):
        selenium_webdriver = None
        try:
            params = {}
            if '?' in scraping_url:
                url_params = scraping_url.split('?')[1].split('&')
                for param in url_params:
                    param_info = param.split('=')
                    if len(param_info) == 2:
                        params.update({decode_string(param_info[0]): decode_string(param_info[1])})
            selenium_webdriver = SeleniumWebDriver(headless=True)
            driver = selenium_webdriver.driver
            location = Location.objects.filter(country='australia').first()
            ebay_domain = EbayDomain.objects.filter(name='ebay.com.au').first()
            category = Category.objects.filter(ebay_category_id=9355).first()
            driver.get(scraping_url)
            time.sleep(5)
            mobile_phones_objects = []
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
                        product_url = item.find_elements(By.CSS_SELECTOR, 'div.s-item__info > a')
                        if not product_url:
                            product_url = item.find_elements(By.CSS_SELECTOR, 'span.bsig__title > a')
                        product_url = product_url[0].get_attribute('href')
                        if 'itm' in product_url:
                            ebay_item_id = int(product_url.split('?')[0].split('itm/')[1])    
                        else:
                            ebay_item_id = int(product_url.split('?')[0].split('p/')[1])
                        product_url_params = [url_params for url_params in product_url.split('?')[1].split('&') if 'itmmeta' not in url_params]
                        product_url = f"{product_url.split('?')[0]}?{'&'.join(product_url_params)}"
                        sold_price = item.find_elements(By.CSS_SELECTOR, 'span.s-item__price')
                        if not sold_price:
                            sold_price = item.find_elements(By.CSS_SELECTOR, 'span.bsig__price')
                        sold_price = sold_price[0].text.split('-')[0].replace('AU $', '').strip()
                        if ' to ':
                            sold_price = sold_price.split(' to ')[0].replace(',', '')
                        if sold_price.lower() == 'free':
                            sold_price = 0.0
                        else:
                            sold_price = float(sold_price)
                        shipping_fee = item.find_elements(By.CSS_SELECTOR, 'span.s-item__shipping')
                        if not shipping_fee:
                            shipping_fee = item.find_elements(By.CSS_SELECTOR, 'span.bsig__logisticsCost')
                        if shipping_fee:
                            shipping_fee = shipping_fee[0].text.replace(',', '')
                            if shipping_fee.lower() == 'free':
                                shipping_fee = 0.0
                            else:
                                shipping_fee = shipping_fee.split(' postage')[0].replace('AU $', '').strip()
                                shipping_fee = float(shipping_fee)
                        if is_sold_listing == True:
                            sold_date = item.find_elements(By.CSS_SELECTOR, 'span.s-item__pl > span > span')
                            if sold_date:
                                sold_date = sold_date[0].get_attribute('data-w')
                                sold_date = format_date(sold_date)
                            else:
                                sold_date = ''
                        model = params.get('Model', None)
                        if not model:
                            data_available = False
                            break
                        product_model = ProductModelCategory.objects.filter(product_model__name=model).first()
                        if not product_model:
                            product_model = self.create_product_model(model, category)
                        brand = BrandCategory.objects.filter(brand__name=params.get('Brand', '')).first()
                        if not brand:
                            brand = self.create_brand(params.get('Brand', ''), category)
                        color = ColorCategory.objects.filter(color__name=params.get('Colour', '')).first()
                        if not color:
                            color = self.create_color(params.get('Colour', ''), category)
                        storage = Storage.objects.filter(value=params.get('Storage Capacity', '')).first()
                        if not storage:
                            storage = self.create_storage(params.get('Storage Capacity', ''))
                        condition = Condition.objects.filter(ebay_condition_id=params.get('LH_ItemCondition', '')).first()
                        lock_status = LockStatus.objects.filter(name=params.get('Lock Status', '')).first()
                        if not lock_status:
                            lock_status = self.create_lock_status(params.get('Lock Status', ''))
                        if is_sold_listing == True:
                            mobile_phone = MobilePhone(title=title, sold_price=sold_price, shipping_fee=shipping_fee, ebay_item_id=ebay_item_id,
                            product_url=product_url, image=image, category=category, product_model=product_model, brand=brand, color=color, storage=storage, lock_status=lock_status,
                            location=location, ebay_domain=ebay_domain, condition=condition, sold_date=sold_date, scraping_url=scraping_url)
                        else:
                            mobile = ActiveMobilePhone.objects.filter(product_url=product_url).first()
                            if mobile:
                                # if active mobile exist, then update the price and shipping fee of product
                                mobile.price = sold_price
                                mobile.shipping_fee = shipping_fee
                                mobile.save()
                                continue
                            mobile_phone = ActiveMobilePhone(title=title, sold_price=sold_price, shipping_fee=shipping_fee, ebay_item_id=ebay_item_id,
                            product_url=product_url, image=image, category=category, product_model=product_model, brand=brand, color=color, storage=storage, lock_status=lock_status,
                            location=location, ebay_domain=ebay_domain, condition=condition, scraping_url=scraping_url)
                        mobile_phones_objects.append(mobile_phone)
                    next_btn = driver.find_elements(By.CSS_SELECTOR, 'a.pagination__next')
                    if next_btn:
                        driver.get(next_btn[0].get_attribute('href'))
                    else:
                        data_available = False
                    time.sleep(3)
                    print(mobile_phones_objects)
                except Exception as e:
                    print('error occur in scrap data =>',e)
                    data_available = False
                    break 
            if mobile_phones_objects:
                if is_sold_listing == True:
                    MobilePhone.objects.bulk_create(mobile_phones_objects, ignore_conflicts=True, batch_size=100)    
                else:
                    ActiveMobilePhone.objects.bulk_create(mobile_phones_objects, ignore_conflicts=True, batch_size=100)
            selenium_webdriver.close()
            return True
        except Exception as e:
            if selenium_webdriver:
                selenium_webdriver.close()
            print('Exception occured during scraping', e)
            return False

    def create_product_model(self, model_name, category):
        try:
            product_model_category = None
            if model_name:
                product_model = ProductModel.objects.filter(name=model_name)
                if product_model:
                    product_model = product_model.first()
                else:
                    product_model = ProductModel.objects.create(name=model_name)
                product_model_category = ProductModelCategory(product_model=product_model, category=category)
            return product_model_category
        except Exception as e:
            print('error occur in creating product model', e)
            return None
            
    def create_brand(self, brand_name, category):
        brand_category = None
        if brand_name:
            brand = Brand.objects.create(name=brand_name)
            brand_category = BrandCategory.objects.create(brand=brand, category=category)
        return brand_category
    
    def create_color(self, color_name, category):
        color_category = None
        if color_name:
            color = Color.objects.create(name=color_name)
            color_category = ColorCategory.objects.create(color=color, category=category)
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
