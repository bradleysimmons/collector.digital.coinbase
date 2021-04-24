from auth import Auth
import requests
import json

class Client(object):

    def __init__(self):
      
        self.API_URL = 'https://api.pro.coinbase.com/'
        self.session = requests.session()
        self.response = None
        self.auth = Auth()

    def _get(self, query_string):
        self.response = self.session.get(self.API_URL + query_string, auth=self.auth)

    def _post(self, end_point, data):
        self.response = self.session.post(self.API_URL + end_point, json=data, auth=self.auth)

    def _delete(self, query_string):
        self.response = self.session.delete(self.API_URL + query_string, auth=self.auth)

    def _handle_response(self):
        if not (200 <= self.response.status_code < 300):
            raise Exception(self.response.status_code)
        try:
            return self.response.json()
        except ValueError:
            raise Exception(self.response.text)

    def get_accounts(self):
        self._get('accounts')
        return [{x['currency']: x['balance']} for x in self._handle_response()]

    def get_products(self, quote_currency=None):
        self._get('products')
        if quote_currency:
            return [x for x in self._handle_response() if x['quote_currency'] == quote_currency]
        else: return self._handle_response()

    def get_user_id(self):
        self._get('profiles')
        return self._handle_response()[0]['user_id']

