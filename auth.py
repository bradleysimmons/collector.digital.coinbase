from config import API_KEY, API_SECRET, API_PASS

import hashlib
import hmac
import requests
import base64
import time
from requests.auth import AuthBase

class Auth(AuthBase):
    def __init__(self):
        self.API_KEY = API_KEY
        self.API_SECRET = API_SECRET
        self.API_PASS = API_PASS

    def __call__(self, request):
        timestamp = str(time.time())
        message = (timestamp + request.method + request.path_url).encode("utf-8")
        if request.body:
            message=b''.join([message, request.body])
       
        request.headers.update(self.get_auth_headers(timestamp, message))

        return request

    def get_auth_headers(self, timestamp, message):
        hmac_key = base64.b64decode(self.API_SECRET)
        signature = hmac.new(hmac_key, message, hashlib.sha256)
        signature_b64 = base64.b64encode(signature.digest()).decode('utf-8')
        return {
            'Content-Type': 'application/json',
            'CB-ACCESS-SIGN': signature_b64,
            'CB-ACCESS-TIMESTAMP': timestamp,
            'CB-ACCESS-KEY': self.API_KEY,
            'CB-ACCESS-PASSPHRASE': self.API_PASS
        }