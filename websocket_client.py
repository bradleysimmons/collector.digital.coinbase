import asyncio
import websockets
import json
import time
from auth import Auth

class CoinbaseWebsocket():
    def __init__(self, portfolio, user_id):
        self.auth = Auth()
        self.url = 'wss://ws-feed.pro.coinbase.com'
        self.portfolio = portfolio
        self.products_dict = {product.data['product_id']: product for product in portfolio.products}
        self.product_ids = list(self.products_dict.keys())
        self.user_id = user_id
        self.channels = [
            {"name": "ticker", "product_ids": self.product_ids},
            {"name": "user", "product_ids": self.product_ids}
        ]

    async def init_websocket(self):
        uri = "wss://ws-feed.pro.coinbase.com"
        async with websockets.connect(uri) as websocket:

            timestamp = str(time.time())
            message = timestamp + 'GET' + '/users/self/verify'
            auth_headers = Auth().get_auth_headers(timestamp, message.encode('ascii'))
            
            params = {
                'type': 'subscribe', 
                'product_ids': self.product_ids, 
                'channels': self.channels,
                'signature': auth_headers['CB-ACCESS-SIGN'],
                'key': auth_headers['CB-ACCESS-KEY'],
                'passphrase': auth_headers['CB-ACCESS-PASSPHRASE'],
                'timestamp': auth_headers['CB-ACCESS-TIMESTAMP']
            }
            
            await websocket.send(json.dumps(params))

            while True:
                message = await websocket.recv()
                self.portfolio.handle_ticker_message(message)

    def run(self):
        asyncio.get_event_loop().run_until_complete(self.init_websocket())
        asyncio.get_event_loop().run_forever()