import asyncio
import websockets
import json
import time
from auth import Auth

class WebsocketClient():
    def __init__(self, portfolio):
        self.auth = Auth()
        self.url = 'wss://ws-feed.pro.coinbase.com'
        self.portfolio = portfolio
        self.products_dict = {product.product_id: product for product in portfolio.products}
        self.product_ids = list(self.products_dict.keys())
        self.channels = [
            {"name": "ticker", "product_ids": self.product_ids},
            {"name": "user", "product_ids": self.product_ids}
        ]

    async def init_websocket(self):
        uri = "wss://ws-feed.pro.coinbase.com"
        while True:
            print('connecting')
            try:
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
                        try:
                            message = await websocket.recv()
                            self.portfolio.handle_ticker_message(json.loads(message))
                        except (asyncio.TimeoutError, websockets.exceptions.ConnectionClosed):
                            try:
                                pong = await websocket.ping()
                                await asyncio.wait_for(pong)
                                print('pong success')
                                continue
                            except:
                                print('pong fail')
                                await asyncio.sleep(5)
                                break
            except Exception as e:
                print('reconnect failed:')
                print(e)
                await asyncio.sleep(5)
                continue



