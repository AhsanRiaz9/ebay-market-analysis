from slack import WebClient
from slack.errors import SlackApiError
import datetime
import os

from dotenv import load_dotenv

load_dotenv('.env')

SLACK_BOT_TOKEN = os.environ.get('SLACK_BOT_TOKEN')
SLACK_BOT_ENABLED = True

def send_message(channel_id, message_text):
    if SLACK_BOT_ENABLED:
        client = WebClient(token=SLACK_BOT_TOKEN)
        try:
            response = client.chat_postMessage(
                channel=f'#{channel_id}',
                text=message_text)
        except SlackApiError as e:
            # You will get a SlackApiError if "ok" is False
            print(f"Got an error: {e.response['error']}")


def generate_mobile_phone_scraping_report(ebay_category_id, current_condition, current_mobile_phone, mobile_data, listing_type, scraping_status):
    current_timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    report_message = f"""
    📱 *Mobile Phone Scraping Report* 📱

    🕒 *Timestamp:* {current_timestamp} 

    📂 *eBay Category ID:* {ebay_category_id}

    * *Sold Items Report:* *
    *Total Mobile Phones Scraped:* {mobile_data['sold_items']['total_scraped']}
    *Total Scraped Today:* {mobile_data['sold_items']['today_scraped']}
    *Scraped in Last 20 Minutes:* {mobile_data['sold_items']['last_20_minutes_scraped']}
    
    * *Buy It Now Items Report:* *
    *Total Mobile Phones Scraped:* {mobile_data['buy_it_now_items']['total_scraped']}
    *Total Scraped Today:* {mobile_data['buy_it_now_items']['today_scraped']}
    *Scraped in Last 20 Minutes:* {mobile_data['buy_it_now_items']['last_20_minutes_scraped']}
    
    *Currently Scraping:* {current_mobile_phone}
    *Condition:* {current_condition}
    *Listing Type:* {listing_type}

    🔄 *Scraping Status:* {scraping_status}

    Thank you for staying updated. Let's keep up the great work! 🚀
    """
    send_message('ebay-marketing-analysis', report_message)

