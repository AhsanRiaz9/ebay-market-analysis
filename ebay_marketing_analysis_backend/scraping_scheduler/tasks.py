from celery import shared_task
from product_configuration.models import Category
from scraping_scheduler.models import ScrapingProcess, MobileScrapingProcess
from django.utils import timezone
from datetime import timedelta
from ebay_products.models import MobilePhone
import os
import requests

@shared_task
def mobile_phone_scraping_scheduler(category_id, new_process=False, first_process=False):
    print('hitting mobile phone scheduler')
    category = Category.objects.filter(ebay_category_id=category_id).first()
    if first_process:
        request_scraping(category_id)
    else:
        last_20_minutes = timezone.now() - timedelta(minutes=20)
        mobile_phones = MobilePhone.objects.filter(created_at__gte=last_20_minutes)
        if not mobile_phones:    
            scraping_process = ScrapingProcess.objects.filter(category=category).first()
            if scraping_process:    
                if scraping_process.is_completed == True and new_process == True:
                    ScrapingProcess.objects.filter(category=category).update(is_complted=False)
                    MobileScrapingProcess.objects.filter(scraping_process=scraping_process).update(is_completed=False, mobile_model='')
                scraping_process = ScrapingProcess.objects.filter(category=category, is_completed=False).first()
                if scraping_process:
                    request_scraping(category_id)
            else:
                request_scraping(category_id)

def request_scraping(category_id):
    try:
        os.system('killall -9 chrome')
        resp = requests.get(f'http://127.0.0.1:8000/ebay_products/download_products/{category_id}/')
        print(resp)
    except Exception as e:
        print(f'Error occurred: {str(e)}')
            
try:
    mobile_phone_scraping_scheduler.delay(category_id=9355, new_process=True, first_process=True)
except Exception as e:
    print(f'Error occurred: {str(e)}')