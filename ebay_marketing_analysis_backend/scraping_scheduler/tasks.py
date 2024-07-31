from celery import shared_task
from product_configuration.models import Category
from scraping_scheduler.models import ScrapingProcess, MobileScrapingProcess
from django.utils import timezone
from datetime import timedelta
from ebay_products.models import MobilePhone, ActiveMobilePhone
import os
import requests
import datetime
from settings.utilis.slack_bot import generate_mobile_phone_scraping_report

@shared_task
def mobile_phone_scraping_scheduler(category_id, new_process=False, first_process=False):
    print('hitting mobile phone scheduler')
    category = Category.objects.filter(ebay_category_id=category_id).first()
    mobile_data = {
        'sold_items': mobile_analytics(True),
        'buy_it_now_items': mobile_analytics(False),
    }    
    last_20_minutes_scraped = mobile_data['sold_items']['last_20_minutes_scraped'] + mobile_data['buy_it_now_items']['last_20_minutes_scraped']
    if first_process:
        request_scraping(category_id)
    else:
        if not last_20_minutes_scraped: 
            scraping_process = ScrapingProcess.objects.filter(category=category).first()
            if scraping_process:
                if scraping_process.is_completed == True and new_process == True:
                    ScrapingProcess.objects.filter(category=category).update(is_completed=False)
                    MobileScrapingProcess.objects.filter(scraping_process=scraping_process).update(is_completed=False, mobile_model='')
                scraping_process = ScrapingProcess.objects.filter(category=category, is_completed=False).first()
                if scraping_process:
                    request_scraping(category_id)
            else:
                request_scraping(category_id)
    scraping_process = ScrapingProcess.objects.filter(category=category).first()
    if scraping_process:
        scraping_status = 'Completed' if scraping_process.is_completed else 'In Completed'
        mobile_phone_scraping = MobileScrapingProcess.objects.filter(scraping_process=scraping_process, is_completed=False).first()
        if mobile_phone_scraping:
            ebay_condition = mobile_phone_scraping.condition.ebay_condition_id
            mobile_model = mobile_phone_scraping.mobile_model
            listing_type = 'Sold Items' if mobile_phone_scraping.is_sold_listing else 'But It Now Items'
        else:
            ebay_condition = ''
            mobile_model = ''
            listing_type = ''
        generate_mobile_phone_scraping_report(category_id, ebay_condition, mobile_model, mobile_data, listing_type, scraping_status)

def mobile_analytics(is_sold_listing):
    today = str(datetime.datetime.now())[:10]
    last_20_minutes = timezone.now() - timedelta(minutes=20)
    if is_sold_listing == True:
        total_mobile_phones = MobilePhone.objects.all()
    else:
        total_mobile_phones = ActiveMobilePhone.objects.all()
    today_scraped_phones = total_mobile_phones.filter(created_at__gte=today)
    last_20_minutes_scraped = total_mobile_phones.filter(created_at__gte=last_20_minutes)
    return {'total_scraped': total_mobile_phones.count(), 'today_scraped': today_scraped_phones.count(), 'last_20_minutes_scraped': last_20_minutes_scraped.count()}

def request_scraping(category_id):
    try:
        os.system('killall -9 chrome')
        resp = requests.get(f'http://127.0.0.1:8008/ebay_products/download_products/{category_id}/')
        print(resp)
    except Exception as e:
        print(f'Error occurred: {str(e)}')
            
try:
    mobile_phone_scraping_scheduler.delay(category_id=9355, new_process=True, first_process=True)
except Exception as e:
    print(f'Error occurred: {str(e)}')

