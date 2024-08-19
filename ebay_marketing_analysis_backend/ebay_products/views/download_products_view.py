from rest_framework.views import APIView
from rest_framework.response import Response
from settings.utilis.helpers import SeleniumWebDriver, create_encoded_url, format_date, check_internet_connection, create_internet_connection, check_webdriver_close_exception, refresh_ip
from product_configuration.models import ProductModel, BrandCategory, ColorCategory, Category, Storage, ProductModelCategory, Condition, ConditionCategory, LockStatus, Location, Brand, Color
from ebay_products.models import MobilePhone, ActiveMobilePhone, ProductRankCounter
import threading
import copy
from tqdm import tqdm
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup
from selenium.common.exceptions import InvalidArgumentException
from scraping_scheduler.models import ScrapingProcess, MobileScrapingProcess
from settings.utilis.exceptions import NetworkException, WebDriverCloseException
import os

# Create your views here.
class DownloadProductView(APIView):
    def get(self, request, category_id, *args, **kwargs):
        self.selenium_webdriver = None
        os.system('killall -9 chrome')
        time.sleep(2)
        t = threading.Thread(target=self.run_scraping_process, args=[category_id,], daemon=True)
        t.start()
        return Response({'message': f'Background job started to download product data of category {category_id}.'})
    
    def set_up_selenium_webdriver(self):
        self.selenium_webdriver = SeleniumWebDriver(headless=True)
        self.set_postage_location('australia')
        
    def accept_consent_btn(self):
        consent_button = self.selenium_webdriver.driver.find_elements(By.CSS_SELECTOR, 'button.fc-cta-consent')
        if consent_button:
            consent_button[0].click()
            time.sleep(3)
    
    def run_scraping_process(self, category_id):
        attempt = 0
        while attempt <= 10:
            if self.selenium_webdriver:
                self.selenium_webdriver.close()
            print('Starting scraping process.')
            os.system('killall -9 chrome')
            result = self.download_data(category_id)
            status = result['status']
            error_type = result['error_type']
            print(result)
            if status == False:
                if error_type == 'internet_issue':
                    create_internet_connection()
                    attempt += 1
                elif error_type == 'webdriver_close_issue':
                    break
            else:
                break
                
    def download_data(self, category_id):
        try:
            status = True
            msg = 'Download product successfully'
            error_type = None
            url = f'https://www.ebay.com.au/b/{category_id}/'
            category = Category.objects.filter(ebay_category_id=category_id).first()
            if not category:
                raise Exception('No category available.')
            scraping_process = ScrapingProcess.objects.filter(category=category).first()
            if not scraping_process:
                scraping_process = ScrapingProcess.objects.create(category=category)
                conditions = ConditionCategory.objects.filter(category=category)
                mobile_scraping_processes = [MobileScrapingProcess(scraping_process=scraping_process, condition=condition_category.condition, is_sold_listing=condition_category.is_sold_listing) for condition_category in conditions]
                MobileScrapingProcess.objects.bulk_create(mobile_scraping_processes, ignore_conflicts=True)
            if scraping_process.is_completed == True:
                scraping_process.is_completed = False
                scraping_process.save()
                MobileScrapingProcess.objects.filter(scraping_process=scraping_process).update(is_completed=False, mobile_model='')
                product_ranker = ProductRankCounter.objects.filter(category=category).first()
                if product_ranker:
                    product_ranker.value = 0
                    product_ranker.save()
            mobile_processes = MobileScrapingProcess.objects.filter(scraping_process=scraping_process, is_completed=False)
            for mobile_process in mobile_processes:
                mobile_process = MobileScrapingProcess.objects.get(pk=mobile_process.id)
                if mobile_process.is_completed == True:
                    continue
                check_internet_connection()
                self.download_mobile_data(url, mobile_process.id, category)
            mobile_proccesses = MobileScrapingProcess.objects.filter(scraping_process=scraping_process, is_completed=False).first()
            if not mobile_proccesses:
                scraping_process.is_completed = True
                scraping_process.save()
                print("Mobile scrapping process completed successfully.")
        except NetworkException as ne:
            msg = 'Download mobile process stopped due to internet connection lost.'
            status = False
            error_type = 'internet_issue'
        except WebDriverCloseException as web_driver_exception:
            msg = 'Download mobile process stopped due to web driver close.'
            status = False
            error_type = 'webdriver_close_issue'
        except Exception as e:
            msg = str(e)
            status = False
        result = {'message': msg, 'status': status, 'error_type': error_type}
        return result
    
    def get_product_rank(self, category):
        product_ranker = ProductRankCounter.objects.filter(category=category).first()
        return product_ranker
        
    def items_exists(self, encoded_url, attempt=0):
        driver = self.selenium_webdriver.driver
        check_internet_connection()
        try:
            items = driver.find_elements(By.CSS_SELECTOR, 'li.s-item')
            return len(items) > 0
        except WebDriverCloseException as e:
            raise WebDriverCloseException('Webdriver closed.')
        except NetworkException as e:
            raise NetworkException('Internet connection lost.')
        except Exception as e:
            check_webdriver_close_exception(e)
            self.selenium_webdriver.close()
            self.set_up_selenium_webdriver()
            check_internet_connection()
            self.selenium_webdriver.driver.get(encoded_url)
            time.sleep(3)
            if attempt == 0:
                return self.items_exists(encoded_url, attempt+1)
            else:
                return False
    
    def validate_filter_value(self, text):
        excluded_values = ('Not Specified', 'All listings', 'Best Offer')
        if text in excluded_values:
            return False
        if '(' in text or ')' in text:
            return False
        return True
    
    def custom_tab_info(self, encoded_url, tab_name, attempt=0):
        driver = self.selenium_webdriver.driver
        check_internet_connection()
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
                soup = BeautifulSoup(tab_info, features="lxml")
                filter_values = [label.text for label in soup.select('label.field__label > span') if self.validate_filter_value(label.text)]
                print(filter_values)
            self._close_filters(driver)
            return filter_values
        except WebDriverCloseException as e:
            raise WebDriverCloseException('Webdriver closed.')
        except NetworkException as e:
            raise NetworkException('Internet closed')
        except Exception as e:
            check_webdriver_close_exception(e)
            if attempt == 0:
                self.selenium_webdriver.close()
                self.set_up_selenium_webdriver()
                self.selenium_webdriver.driver.get(encoded_url)
                check_internet_connection()
                time.sleep(3)
                return self.custom_tab_info(encoded_url, tab_name, attempt+1)
            else:
                return []
        
    def _open_filters(self, driver):
        check_internet_connection()
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "button[aria-label='All filters']"))
            )
            filter_all_btn = driver.find_elements(By.CSS_SELECTOR, "button[aria-label='All filters']")
            if filter_all_btn:
                filter_all_btn[0].click()
                return True
        except WebDriverCloseException as e:
            raise WebDriverCloseException('Webdriver closed.')
        except NetworkException as e:
            raise NetworkException('Internet closed')
        except Exception as e:
            check_webdriver_close_exception(e)
            print(e)
        return False
    
    def _close_filters(self, driver):
        check_internet_connection()
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '.x-overlay__container>button'))
            )
            overlay_close = driver.find_elements(By.CSS_SELECTOR, '.x-overlay__container>button')
            if overlay_close:
                overlay_close[0].click()
                time.sleep(2)
                return True
        except WebDriverCloseException as e:
            raise WebDriverCloseException('Webdriver closed.')
        except NetworkException as e:
            raise NetworkException('Internet closed')
        except Exception as e:
            check_webdriver_close_exception(e)
            print(e)
        return False
    
    
    
    def download_mobile_data(self, url, mobile_process_id, category):
        check_internet_connection()
        self.set_up_selenium_webdriver()
        self.visit_count = 0
        mobile_process = MobileScrapingProcess.objects.get(id=mobile_process_id)
        listing_types = {
            'buy_it_now': {'LH_BIN': 1,}, 
            'sold_listing': {'LH_Complete': 1, 'LH_Sold': 1, '_sop': 10}
        }
        params = {
            'rt': 'nc', 
            'mag': 1,
            'LH_ItemCondition': mobile_process.condition.ebay_condition_id,
        }
        if mobile_process.is_sold_listing == True:
            params.update(listing_types['sold_listing'])
        else:
            params.update(listing_types['buy_it_now'])
        encoded_url = create_encoded_url(url, params)
        check_internet_connection()
        self.visit_url(encoded_url)
        mobile_phones = self.custom_tab_info(encoded_url, 'Model')
        last_mobile_phone = mobile_process.mobile_model
        if last_mobile_phone and last_mobile_phone in mobile_phones:
            last_mobile_phone_index = mobile_phones.index(last_mobile_phone)
            mobile_phones = mobile_phones[last_mobile_phone_index:]
        total_mobiles = len(mobile_phones)
        count = 0
        for mobile in tqdm(mobile_phones):
            count += 1
            try:
                mobile_process = MobileScrapingProcess.objects.get(id=mobile_process_id)
                mobile_process.mobile_model = mobile
                mobile_process.save()
                if mobile_process.is_completed == True:
                    time.sleep(3)
                    continue
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
                                self.scrap_data(url, params, mobile_process, {'Model': mobile, 'Brand': brand_name, 'Storage Capacity': storage, 'Colour': color, 'Lock Status': lock_status}, category)
            except NetworkException as ne:
                print('Scraping stopped due to =>', ne)
                self.selenium_webdriver.close()
                raise NetworkException('Internet not connected.')
            except WebDriverCloseException as web_driver_close_exception:
                self.selenium_webdriver.close()
                raise WebDriverCloseException('WebDriver closed.')
            except Exception as e:
                continue
        if count == total_mobiles:
            mobile_process.mobile_model = ''
            mobile_process.is_completed = True
            mobile_process.save()    
        self.selenium_webdriver.close()
    
    def visit_url(self, url):
        check_internet_connection()
        try:
            self.visit_count += 1
            close_browser = self.visit_count%20==0
            
            if not close_browser:
                self.selenium_webdriver.driver.get(url)
                time.sleep(3)
            body_text = self.selenium_webdriver.driver.find_element(By.CSS_SELECTOR, 'body').text
            error_msg1 = 'An error occurred while processing your request.'
            error_msg2 = 'Please verify yourself to continue'
            if self.visit_count%20==0 or error_msg1 in body_text or error_msg2 in body_text:
                self.selenium_webdriver.close()
                refresh_ip()
                self.set_up_selenium_webdriver()
                self.selenium_webdriver.driver.get(url)
                time.sleep(3)
        except InvalidArgumentException as e:
            self.selenium_webdriver.close()
            self.set_up_selenium_webdriver()
            self.selenium_webdriver.driver.get(url)
        except WebDriverCloseException as e:
            raise WebDriverCloseException('Webdriver closed.')
        except NetworkException as e:
            raise NetworkException('Internet closed')
        except Exception as e:
            print('Error occur in visit url, exception =>', e)
            check_webdriver_close_exception(e)
        check_internet_connection()
    
    def set_postage_location(self, country):
        print(country)
        driver = self.selenium_webdriver.driver
        for i in range(3):
            driver.get('https://www.ebay.com.au/sch/i.html?_from=R40&_trksid=p4432023.m570.l1313&_nkw=iphone&_sacat=0')
            time.sleep(10)
            self.accept_consent_btn()
            time.sleep(3)
            postage_btn = driver.find_elements(By.CSS_SELECTOR, 'button > span.s-zipcode-entry__label')
            if postage_btn:
                postage_btn[0].click()
                time.sleep(2)
                country_selector = driver.find_elements(By.CSS_SELECTOR, 'div.srp-shipping-location__form--inline select')
                if country_selector:
                    country_selector[0].send_keys(country)
                    post_code = driver.find_element(By.CSS_SELECTOR, "input[autocomplete='postal-code']")
                    post_code.send_keys('2144')
                    time.sleep(1)
                    apply_btn = driver.find_elements(By.CSS_SELECTOR, '.s-zipcode-entry__apply > button.btn--primary')
                    if apply_btn:
                        apply_btn[0].click()
                        time.sleep(3)
                        print(f'Location changed to {country} successfully.')
                        time.sleep(5)
                        break
                              
    def scrap_data(self, url, params, mobile_process, filter_conditions, category):
        driver = self.selenium_webdriver.driver
        location = Location.objects.filter(domain='ebay.com.au').first()
        filter_params = copy.deepcopy(params)
        filter_params.update(filter_conditions)
        encoded_url = create_encoded_url(url, filter_params)
        check_internet_connection()
        self.visit_url(encoded_url)
        time.sleep(3)
        mobile_phones_objects = []
        print(filter_params)
        product_ranker = self.get_product_rank(category)
        rank_vaule = product_ranker.value
        data_available = True
        while data_available:
            try:
                print('data available', data_available)
                check_internet_connection()
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
                    if mobile_process.is_sold_listing == True:
                        sold_date = item.find_elements(By.CSS_SELECTOR, 'span.s-item__pl > span > span')
                        if sold_date:
                            sold_date = sold_date[0].get_attribute('data-w')
                            sold_date = format_date(sold_date)
                        else:
                            sold_date = ''
                    product_model = ProductModelCategory.objects.filter(product_model__name=filter_conditions['Model']).first()
                    if not product_model:
                        product_model = self.create_product_model(filter_conditions['Model'], category)
                    brand = BrandCategory.objects.filter(brand__name=filter_conditions['Brand']).first()
                    if not brand:
                        brand = self.create_brand(filter_conditions['Brand'], category)
                    color = ColorCategory.objects.filter(color__name=filter_conditions['Colour']).first()
                    if not color:
                        color = self.create_color(filter_conditions['Colour'], category)
                    storage = Storage.objects.filter(value=filter_conditions['Storage Capacity']).first()
                    if not storage:
                        storage = self.create_storage(filter_conditions['Storage Capacity'])
                    condition = Condition.objects.filter(ebay_condition_id=params['LH_ItemCondition']).first()
                    lock_status = LockStatus.objects.filter(name=filter_conditions['Lock Status']).first()
                    if not lock_status:
                        lock_status = self.create_lock_status(filter_conditions['Lock Status'])
                    if mobile_process.is_sold_listing == True:
                        mobile_phone = MobilePhone(title=title, sold_price=sold_price, shipping_fee=shipping_fee, ebay_item_id=ebay_item_id,
                        product_url=product_url, image=image, category=category, product_model=product_model, brand=brand, color=color, storage=storage, lock_status=lock_status,
                        location=location, condition=condition, sold_date=sold_date, scraping_url=encoded_url)
                    else:
                        rank_vaule += 1
                        mobile = ActiveMobilePhone.objects.filter(product_url=product_url).first()
                        if mobile:
                            # if active mobile exist, then update the price and shipping fee of product
                            mobile.price = sold_price
                            mobile.shipping_fee = shipping_fee
                            mobile.ranking = rank_vaule
                            mobile.save()
                            continue
                        mobile_phone = ActiveMobilePhone(title=title, sold_price=sold_price, shipping_fee=shipping_fee, ebay_item_id=ebay_item_id, ranking=rank_vaule,
                        product_url=product_url, image=image, category=category, product_model=product_model, brand=brand, color=color, storage=storage, lock_status=lock_status,
                        location=location, condition=condition, scraping_url=encoded_url)
                    mobile_phones_objects.append(mobile_phone)
                next_btn = driver.find_elements(By.CSS_SELECTOR, 'a.pagination__next')
                if next_btn:
                    driver.get(next_btn[0].get_attribute('href'))
                else:
                    data_available = False
                time.sleep(3)
                print(mobile_phones_objects)
            except WebDriverCloseException as e:
                raise WebDriverCloseException('Webdriver closed.')
            except NetworkException as e:
                raise NetworkException('Internet closed')
            except Exception as e:
                print('error occur in scrap data =>',e)
                data_available = False
                break 
        if mobile_phones_objects:
            if mobile_process.is_sold_listing == True:
                MobilePhone.objects.bulk_create(mobile_phones_objects, ignore_conflicts=True, batch_size=100)    
            else:
                ActiveMobilePhone.objects.bulk_create(mobile_phones_objects, ignore_conflicts=True, batch_size=100)
                product_ranker.value = rank_vaule
                product_ranker.save()
            
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