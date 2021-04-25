from threading import Thread
from websocket import create_connection, WebSocketConnectionClosedException
from auth import Auth
import time
import json

class Websocket():
    def __init__(self, products, portfolio, user_id):
        self.auth = Auth()
        self.url = 'wss://ws-feed.pro.coinbase.com'
        self.products_dict = {product.data['product_id']: product for product in products}
        self.portfolio = portfolio
        self.user_id = user_id
        self.channels = [
            {"name": "ticker", "product_ids": list(self.products_dict.keys())},
            {"name": "user", "product_ids": list(self.products_dict.keys())}
        ]
        self.stop = True
        self.error = None
        self.ws = None
        self.thread = None
        

    def start(self):
        def _go():
            self._connect()
            self._listen()
            self._disconnect()

        self.stop = False
        self.on_open()
        self.thread = Thread(target=_go)
        self.keepalive = Thread(target=self._keepalive)
        self.thread.start()

    def _connect(self):  
        sub_params = {'type': 'subscribe', 'product_ids': list(self.products_dict.keys()), 'channels': self.channels}

        timestamp = str(time.time())
        message = timestamp + 'GET' + '/users/self/verify'
        auth_headers = self.auth.get_auth_headers(timestamp, message.encode('ascii'))
        sub_params['signature'] = auth_headers['CB-ACCESS-SIGN']
        sub_params['key'] = auth_headers['CB-ACCESS-KEY']
        sub_params['passphrase'] = auth_headers['CB-ACCESS-PASSPHRASE']
        sub_params['timestamp'] = auth_headers['CB-ACCESS-TIMESTAMP']

        self.ws = create_connection(self.url)

        self.ws.send(json.dumps(sub_params))

    def _keepalive(self, interval=30):
        while self.ws.connected:
            self.ws.ping("keepalive")
            time.sleep(interval)

    def _listen(self):
        self.keepalive.start()
        while not self.stop:
            try:
                data = self.ws.recv()
                msg = json.loads(data)
            except ValueError as e:
                self.on_error(e)
            except Exception as e:
                self.on_error(e)
            else:
                self.on_message(msg)

    def _disconnect(self):
        try:
            if self.ws:
                self.ws.close()
        except WebSocketConnectionClosedException as e:
            pass
        finally:
            self.keepalive.join()

        self.on_close()

    def close(self):
        self.stop = True   
        self._disconnect() 
        self.thread.join()

    def on_open(self):
        print('websocket connected')

    def on_close(self):
        print('websocket closed')

    def on_error(self, e, data=None):
        self.error = e
        self.stop = True

    def on_message(self, msg):
        if msg['type'] in ['ticker']:
            self.products_dict[msg['product_id']].update_data(msg)
            self.portfolio.set_cash_value()

        if msg.get('user_id') == self.user_id and msg['type'] == 'done':
            self.products_dict[msg['product_id']].set_balance()
            self.portfolio.set_cash_value()
            self.portfolio.set_cash_balance()

