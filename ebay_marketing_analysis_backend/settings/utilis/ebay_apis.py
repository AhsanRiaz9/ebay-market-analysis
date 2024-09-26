from urllib.parse import unquote
import base64
import requests
from enum import Enum

class GrantType(Enum):
    CLIENT_CREDENTIALS = 'client_credentials'
    AUTHORIZATION_CODE = 'authorization_code'
    REFRESH_TOKEN = 'refresh_token'

class EbayOAuthService:
    def __init__(self, client_id, client_secret, redirect_uri, scope):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.scope = scope
    
    def __generate_oauth_encoded_key(self, client_id, client_secret):
        concatenated_string = f"{client_id}:{client_secret}"
        encoded_bytes = base64.b64encode(concatenated_string.encode('utf-8'))
        encoded_key = encoded_bytes.decode('utf-8')
        return encoded_key
    
    def generate_access_token(self, grant_type,  code='', refresh_token=''):
        url = 'https://api.ebay.com/identity/v1/oauth2/token'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': f'Basic {self.__generate_oauth_encoded_key(self.client_id, self.client_secret)}',
        }
        payload = {'grant_type': grant_type.value}
        if grant_type != GrantType.REFRESH_TOKEN:
            payload.update({
                'redirect_uri': self.redirect_uri,
                'scope': self.scope,
            })
            if grant_type == GrantType.CLIENT_CREDENTIALS:
                payload.update({'code': unquote(code)})  
        else:
            payload.update({
                'refresh_token': refresh_token  
            })
        response = requests.post(url, data=payload, headers=headers)
        return response

class EbayAPIService:
    def __init__(self, client_id, client_secret, redirect_uri, scope):
        self.ebay_oauth_service = EbayOAuthService(client_id, client_secret, redirect_uri, scope)

    def ebay_search_query(self, access_token, seller_id, limit, offset):
        url = 'https://api.ebay.com/buy/browse/v1/item_summary/search'
        params = {'q': ' ', 'limit': limit, 'offset': offset, 'filter': f'sellers:{{{seller_id}}}'}
        headers = {
            'Authorization': f'Bearer {access_token}',
            'X-EBAY-C-MARKETPLACE-ID': 'EBAY_AU',
        }
        resp = requests.get(url, params=params, headers=headers)
        return resp

    def fetch_ebay_store(self, seller_id):
        # print('Get Access token using client credentials')
        limit = 200
        offset = 0
        resp = self.ebay_oauth_service.generate_access_token(grant_type=GrantType.CLIENT_CREDENTIALS) 
        access_token = resp.json()['access_token']
        print('Access token', access_token)
        pagination_stop = False
        products = []
        categories = {}
        while pagination_stop == False:
            resp = self.ebay_search_query(access_token, seller_id, limit, offset)
            if resp.ok == False:
                access_token = self.ebay_oauth_service.generate_access_token(grant_type=GrantType.CLIENT_CREDENTIALS)
                resp = self.ebay_search_query(access_token, seller_id, limit, offset)
            products_data = resp.json()
            import pdb
            pdb.set_trace()
            if 'warning' in products_data.keys():
                pagination_stop = True
                break
            total_products = products_data.get('total', 0)
            if total_products == 0:
                break
            items = products_data.get('itemSummaries', [])
            for item in items:
                item_categories = {category.get('categoryId'):category.get('categoryName') for category in item.get('categories', [])}
                category_id = item.get('leafCategoryIds')[0]
                category_name = item_categories.get(category_id)
                if category_id not in categories:
                    categories[category_id] = category_name
                item_image = item.get('thumbnailImages', '')
                item_image = item_image[0]['imageUrl'] if item_image else ''
                shipping_cost = item.get('shippingOptions', 0.0)
                if shipping_cost:
                    shipping_cost = shipping_cost[0].get('shippingCost').get('value')
                try:
                    products.append({
                        'title': item['title'],
                        'price': float(item['price']['value']),
                        'url': item.get('itemWebUrl'),
                        'image': item_image,
                        'ebay_item_id': item.get('itemId'),
                        'category_id': category_id,
                        'category_name': category_name,
                        'seller': item.get('seller')['username'],
                        'condition': item.get('conditionId', None),
                        'shipping_cost': shipping_cost,
                    })
                except Exception as e:
                    import pdb
                    pdb.set_trace()
                    print('Error processing product', e)
            if 'next' not in products_data.keys():
                pagination_stop = True
            offset += limit
        result = {'products': products, 'categories': categories}
        return result
