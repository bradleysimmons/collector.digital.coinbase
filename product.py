from decimal import Decimal
from helpers import calculate_delta
import time

class Product():
    def __init__(self, data, client, account, threshold):
        self._init_data(data, account)
        self.client = client
        self.threshold = threshold
        self.buy_wait_until = time.time()
        self.sell_wait_until = time.time()

    def update_data(self, data):
        self.data.update(data)
        self._set_cash_value()

    def set_balance(self):
        self.data['balance'] = self.client.get_balance(self.data['account_id'])

    #string_v returns all string values
    def get_data(self, key=None, string_v=False):
        if key:
            return self.data[key] if not string_v else str(self.data[key])
        else: return self.data if not string_v else {k: str(self.data[k]) for k in self.data}

    def _init_data(self, data, account):
        data['product_id'] = data['id']
        data['id'] = data['id'].replace('-USD', '')
        data['account_id'] = account['id']
        data['balance'] = account['balance']
        data['cash_value'] = Decimal(0)
        data['cash_value_s'] = '0.0'
        self.data = data

    def _set_cash_value(self):
        if self.data.get('price'):
            self.data['cash_value'] = Decimal(self.data['price']) * Decimal(self.data['balance'])
            self.data['cash_value_s'] = str(self.data['cash_value'])

    def update_mean_delta(self, mean):
        if self.data.get('price') and mean:
            self.data['portfolio_mean'] = mean #probably should be in portfolio class, but this is convenient
            self.data['mean_delta'] = calculate_delta(mean, self.data['cash_value'])

    def check_threshold(self):
        if self.data.get('price') and self.data.get('portfolio_mean'):
            if (Decimal(self.data['balance']) == Decimal(0) #dont have any
                and self.buy_wait_until < time.time()): #no requests out
                self._buy()
            if self.data.get('mean_delta'):
                if (self.data['mean_delta'] >= self.threshold
                    and self.sell_wait_until < time.time()):
                    self._sell()
                if (self.data['mean_delta'] <= self.threshold * -1 #threshold is low
                    and self.buy_wait_until < time.time()): #no requests out
                    self._buy()     

    def _get_sell_price(self):
        return Decimal(self.data['best_ask']) - Decimal(self.data['quote_increment'])

    def _get_sell_quantity(self, price):
        amount_over_mean = Decimal(self.data['cash_value']) - Decimal(self.data['portfolio_mean'])
        return amount_over_mean / price

    def _get_buy_price(self):
        return Decimal(self.data['best_bid']) + Decimal(self.data['quote_increment'])

    def _get_buy_quantity(self, price):
        amount_under_mean = Decimal(self.data['portfolio_mean']) - Decimal(self.data['cash_value'])
        return amount_under_mean / price

    def _buy(self):
        price = self._get_buy_price()
        quantity = self._get_buy_quantity(price)
        print('buy')
        print(self.data['product_id'])
        print(price)
        print(quantity)

    def _sell(self):
        price = self._get_sell_price()
        quantity = self._get_sell_quantity(price)
        print('sell')
        print(self.data['product_id'])
        print(price)
        print(quantity)
            

