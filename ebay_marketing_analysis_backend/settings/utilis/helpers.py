import requests
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from settings.utilis.exceptions import NetworkException, WebDriverCloseException
import undetected_chromedriver as uc
import os

class SeleniumWebDriver:
    def __init__(self, headless=True):
        self.driver = self._configure_webdriver(headless)
        
    def _configure_webdriver(self, headless):
        options = Options()
        self._configure_chrome_options(options, headless)
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
        options.add_argument(f'user-agent={user_agent}')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument("--start-maximized")
        options.add_argument("--incognito")
        return uc.Chrome(options=options)

    @staticmethod
    def _configure_chrome_options(options, headless):
        if headless:
            options.add_argument('--headless=new')
        options.add_argument('--no-sandbox')

    def close(self):
        try:
            self.driver.close()
        except:
            pass

def refresh_ip():
    os.system('expressvpn disconnect')
    os.system(f"expressvpn connect 'Pakistan'")
    time.sleep(4)

def encode_string(input_string):
    input_string = str(input_string)
    conversion_codes = {'+': '%252B', '.': '%252E', ' ': '%2520', ',': '%7C', '&': '%2526', '-': '%252D', '(': '%2528', ')': '%2529', '/': '%252F'}
    translated_string = input_string.translate(str.maketrans(conversion_codes))
    return translated_string
        
def create_encoded_url(url, params):
    params_value = [f'{encode_string(key)}={encode_string(value)}' for key, value in params.items()]
    query_string = '&'.join(params_value)
    if not '?' in url:
        encoded_url = f'{url}?{query_string}'   
    else:
        encoded_url = f'{url}{query_string}'
    return encoded_url

def format_date(date_str):
    date_str = date_str.replace('SOLD  ', '')
    date_info = date_str.split(' ')
    month_dict = {'jan': '01', 'feb': '02', 'mar': '03', 'apr': '04', 'may': '05', 'jun': '06', 'jul': '07', 'aug': '08', 'sep': '09', 'oct': '10', 'nov': '11', 'dec': '12'}
    day = date_info[0]
    if len(day) == 1:
        day = f'0{day}'
    month = date_info[1].lower()
    year = date_info[2]
    formated_date = f'{year}-{month_dict[month]}-{day}'
    return formated_date

def check_internet_connection():
    count = 0
    for i in range(3):
        try:
            time.sleep(2)
            requests.get('https://www.google.com')
            return
        except Exception as e:
            count += 1
            if count == 3:
                raise NetworkException('Connection is not established.')

def create_internet_connection():
    attempt = 0
    internet_status = False
    while internet_status == False and attempt <= 30:
        internet_status = is_internet_available()
        if not internet_status:
            attempt += 1
    return internet_status
            
def is_internet_available():
    try:
        time.sleep(2)
        requests.get('https://www.google.com')
        print('Internet connection established successfully.')
        return True
    except Exception as e:
        print('Internet is not connected. Waiting for connection.')
        return False

def check_webdriver_close_exception(e):
    if 'no such window: target window already closed' in str(e):
        raise WebDriverCloseException('Web driver closed. Scraping stopped.')