from product import Product
from decimal import Decimal
import time
from config import threshold

class Portfolio():
    def __init__(self, products, accounts, client, seed, user_id):
        self.products = [Product(x, client, accounts[x['base_currency']], threshold, self) for x in products]
        self.products_dict = {product.data['product_id']: product for product in self.products}
        self.cash_balance = accounts['USD']['balance']
        self.usd_account_id = accounts['USD']['id']
        self.user_id = user_id
        self.client = client
        self.set_cash_value()
        self.set_portfolio_balance()
        self.wait_until = time.time()
        self.is_trade_ready = False
        self.seed = seed
        
    # to send out to react client
    def get_websocket_data(self):
        return {
            'products': [x.get_data(string_v=True) for x in self.products],
            'portfolio': {'portfolio_balance': str(self.portfolio_balance),
                            'cash_value': str(self.cash_value),
                            'cash_balance': self.cash_balance}
        }

    def set_portfolio_balance(self):
        self.portfolio_balance = self.cash_value + Decimal(self.cash_balance)

    def set_cash_value(self):
        self.cash_value = sum(x.get_data(key='cash_value') for x in self.products)

    def set_cash_balance(self):
        self.cash_balance = self.client.get_balance(self.usd_account_id)

    def set_mean_value(self):
        self.mean_value = self.cash_value / len(self.products)

    def _get_target_mean(self):
        return self.portfolio_balance / len(self.products)

    # set the wait until value so only one order is out at time, based off 1 min limit orders
    def set_wait_until(self, value):
        self.wait_until = value

    # safety to make sure every product has a price before stuff happens
    def get_is_trade_ready(self):
        if self.is_trade_ready == True: return True
        if all([x.get_data(key='price') for x in self.products]):
            self.is_trade_ready = True
            if self.seed: self.seed_it()
            return True
        return False

    # starting with cash and no held products
    def seed_it(self):
        for product in self.products: 
            product.seed()

    def handle_ticker_message(self, message):
        print(message['type'])
        if message['type'] in ['ticker']:
            self.products_dict[message['product_id']].update_data(message)
            self.set_cash_value()
            self.set_portfolio_balance()
            self.set_mean_value()
            self.products_dict[message['product_id']].update_mean_delta()
            self.products_dict[message['product_id']].check_threshold()

        if message.get('user_id') == self.user_id and message['type'] == 'done':
            self.products_dict[message['product_id']].set_balance()
            self.set_cash_value()
            self.set_cash_balance()
            self.set_portfolio_balance()
            self.set_wait_until(time.time())





