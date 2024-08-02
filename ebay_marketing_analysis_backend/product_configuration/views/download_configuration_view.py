from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from settings.utilis.helpers import SeleniumWebDriver, create_encoded_url
from product_configuration.models import Category, Brand, BrandCategory, Color, ColorCategory, LockStatus, Storage, ProductModel, ProductModelCategory, Condition, ConditionCategory, Filter, FilterCategory, Location
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import threading
import pandas as pd
import io
import time
from tqdm import tqdm
from scraping_scheduler.models import ScrapingProcess, MobileScrapingProcess
from ebay_products.models import ProductRankCounter

# Create your views here.
class LoadProductConfiguration(APIView):
    
    def get(self, request, category_id, *args, **kwargs):
        t = threading.Thread(target=self.download_data, args=[category_id,],daemon=True)
        t.start()
        return Response({'message': f'Background job started to save product configuration for category {category_id}.'})
    
    def download_data(self, category_id):
        try:
            selenium_webdriver = SeleniumWebDriver(headless=True)
            driver = selenium_webdriver.driver
            url = f'https://www.ebay.com.au/b/{category_id}/?LH_Complete=1&LH_Sold=1&rt=nc&LH_BIN=1&mag=1'
            driver.get(url)
            category = Category.objects.filter(ebay_category_id=category_id)
            if not category.exists():
                category_name = driver.find_element(By.CSS_SELECTOR, 'h1.b-pageheader').text
                category = Category.objects.create(name=category_name, ebay_category_id=category_id)
            else:
                category = category[0]
            product_ranker = ProductRankCounter.objects.filter(category=category).first()
            if not product_ranker:
                product_ranker = ProductRankCounter.objects.create(category=category)
            time.sleep(3)
            self.download_filters_data(driver, category)
            self.download_brands_data(driver, category)
            self.download_colours_data(driver, category)
            self.download_models_data(driver, category)
            self.download_lock_statuses_data(driver)
            self.download_storage_capacity_data(driver)
            self.download_conditions_data(driver, category)
            self.create_scraping_process(category)
        except Exception as e:
            print(e)
            selenium_webdriver.close()

    
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
    
    def validate_filter_value(self, text):
        excluded_values = ('Not Specified', 'All listings', 'Best Offer')
        if text in excluded_values:
            return False
        if '(' in text or ')' in text:
            return False
        return True

    def custom_tab_info(self, driver, tab_name):
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
    
    def download_filters_data(self, driver, category):
        try:
            self._open_filters(driver)
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div[role="tab"]'))
            )
            filters_tabs = [filter_tab.text for filter_tab in driver.find_elements(By.CSS_SELECTOR, 'div[role="tab"]')]
            filters_objects = [Filter(name=filter_name) for filter_name in filters_tabs]
            Filter.objects.bulk_create(filters_objects, ignore_conflicts=True, batch_size=500)
            filter_category_objects = []
            for filter_name in filters_tabs:
                filter = Filter.objects.get(name=filter_name)
                filter_category_objects.append(FilterCategory(filter=filter, category=category))
            FilterCategory.objects.bulk_create(filter_category_objects, ignore_conflicts=True, batch_size=500)
            self._close_filters(driver)
        except Exception as e:
            print(e)
    
    def download_brands_data(self, driver, category):
        try:
            brands_data = self.custom_tab_info(driver, 'Brand')
            brand_objects = [Brand(name=brand) for brand in brands_data]
            Brand.objects.bulk_create(brand_objects, ignore_conflicts=True, batch_size=500)
            brand_category_objects = []
            for name in brands_data:
                brand = Brand.objects.get(name=name)
                brand_category_objects.append(BrandCategory(brand=brand, category=category))
            BrandCategory.objects.bulk_create(brand_category_objects, ignore_conflicts=True, batch_size=500)
        except Exception as e:
            print(e)

    def download_models_data(self, driver, category):
        try:
            models_data = self.custom_tab_info(driver, 'Model')
            product_models_objects = [ProductModel(name=model) for model in models_data]
            ProductModel.objects.bulk_create(product_models_objects, ignore_conflicts=True, batch_size=500)
            product_models_category_objects = [] 
            for name in tqdm(models_data):
                model = ProductModel.objects.get(name=name)
                product_models_category_objects.append(
                    ProductModelCategory(product_model=model, category=category)
                )
            ProductModelCategory.objects.bulk_create(product_models_category_objects, ignore_conflicts=True, batch_size=500)
        except Exception as e:
            print(e)
        
    def download_colours_data(self, driver, category):
        try:
            colors_data = self.custom_tab_info(driver, 'Colour')
            color_objects = [Color(name=color) for color in colors_data]
            Color.objects.bulk_create(color_objects, ignore_conflicts=True, batch_size=500)
            color_category_objects = []
            for name in colors_data:
                color = Color.objects.get(name=name)
                color_category_objects.append(ColorCategory(color=color, category=category))
            ColorCategory.objects.bulk_create(color_category_objects, ignore_conflicts=True, batch_size=500)
        except Exception as e:
            print(e)            
            
    def download_lock_statuses_data(self, driver):     
        try:
            lock_status_data = self.custom_tab_info(driver, 'Lock Status')
            lock_status_objects = [LockStatus(name=name) for name in lock_status_data]
            LockStatus.objects.bulk_create(lock_status_objects, ignore_conflicts=True, batch_size=500)
        except Exception as e:
            print(e)

    def download_storage_capacity_data(self, driver):     
        try:
            storage_data = self.custom_tab_info(driver, 'Storage Capacity')
            storage_objects = [Storage(value=storage) for storage in storage_data]
            Storage.objects.bulk_create(storage_objects, ignore_conflicts=True, batch_size=500)
        except Exception as e:
            print(e)
    
    def download_conditions_data(self, driver, category):
        url = f'https://www.ebay.com.au/b/{category.ebay_category_id}/'
        conditions = Condition.objects.all()
        condition_categories_objects = []
        listing_types = {
            'buy_it_now': {'LH_BIN': 1,}, 
            'sold_listing': {'LH_Complete': 1, 'LH_Sold': 1}
        }
        for key in listing_types.keys():
            sold_flag = True if key == 'sold_listing' else False
            for condition in conditions:
                params = {
                    'rt': 'nc', 
                    'mag': 1,
                    'LH_ItemCondition': condition.ebay_condition_id
                }
                params.update(listing_types[key])
                encoded_url = create_encoded_url(url, params)
                driver.get(encoded_url)
                time.sleep(5)
                items = driver.find_elements(By.CSS_SELECTOR, 'li.s-item')
                if len(items) != 0:
                    condition_categories_objects.append(ConditionCategory(condition=condition, category=category, is_sold_listing=sold_flag))                
            if condition_categories_objects:
                ConditionCategory.objects.bulk_create(condition_categories_objects, ignore_conflicts=True, batch_size=500)

    def create_scraping_process(self, cateogry):
        condition_categories = ConditionCategory.objects.filter(category=cateogry)
        scraping_process = ScrapingProcess.objects.filter(category=cateogry).first()
        if not scraping_process:
            scraping_process = ScrapingProcess.objects.create(cateogry=cateogry)
        mobile_scraping_processes = [MobileScrapingProcess(scraping_process=scraping_process, condition=condition_category.condition, is_sold_listing=condition_category.is_sold_listing) for condition_category in condition_categories]
        MobileScrapingProcess.objects.bulk_create(mobile_scraping_processes, ignore_conflicts=True, batch_size=100)
        
class DownloadEbayCondtions(APIView):
    def get(self, request, *args, **kwargs):
        t = threading.Thread(target=self.download_data, args=[],daemon=True)
        t.start()
        return Response({'message': f'Background job started to save ebay condition data.'})
    
    def download_data(self):
        try:  
            selenium_webdriver = SeleniumWebDriver(headless=True)
            driver = selenium_webdriver.driver
            url = 'https://www.edp.ebay.com/devzone/finding/CallRef/Enums/conditionIdList.html'
            driver.get(url)
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "table.tableEnum"))
            )
            html_table = driver.find_element(By.CSS_SELECTOR, "table.tableEnum")
            table = pd.read_html(io.StringIO(html_table.get_attribute('outerHTML')))[0]
            selenium_webdriver.close()
            size = len(table)
            condition_objects = [Condition(name=table['Typical Name'][i], ebay_condition_id=table['ID'][i]) for i in range(size)]
            Condition.objects.bulk_create(condition_objects, ignore_conflicts=True, batch_size=500)
        except Exception as e:
            print(e)

class DownloadEbayLocations(APIView):
    
    def get(self, request):
        status = True
        message = 'Location downloaded successfully!'
        try:
            df = pd.read_csv('product_configuration/locations.csv')
            size = len(df)
            location_objects = []
            for i in range(size):
                location_objects.append(Location(domain=df['domain'][i], country=df['country'][i]))
            Location.objects.bulk_create(location_objects, ignore_conflicts=True, batch_size=500)
        except Exception as e:
            print(e)
            status = False
            message = 'Error while downoading location data.'
        return Response({'message': message, 'status': status})