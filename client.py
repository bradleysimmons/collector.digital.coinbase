from auth import Auth
import requests

class Client(object):

    def __init__(self):
      
        self.API_URL = 'https://api.pro.coinbase.com/'
        self.auth = Auth()


    def _get(self, query_string):
        return requests.get(self.API_URL + query_string, auth=self.auth)

    def _post(self, end_point, data):
        return requests.post(self.API_URL + end_point, json=data, auth=self.auth)

    def _delete(self, query_string):
        return requests.delete(self.API_URL + query_string, auth=self.auth)

    def get_accounts(self):
        return self._get('accounts')

