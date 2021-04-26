from decimal import Decimal
from helpers import calculate_delta
import time

class Product():
    def __init__(self, data, client, account, threshold):
        self._init_data(data, account)
        self.client = client
        self.threshold = threshold

    # data is a dict, just update directly from ticket websocket
    def update_data(self, data):
        self.data.update(data)
        self._set_cash_value() # calculation based on price

    def set_balance(self):
        self.data['balance'] = self.client.get_balance(self.data['account_id'])

    #string_v returns all string values, for outgoing websocket
    def get_data(self, key=None, string_v=False):
        if key:
            return self.data.get(key) if not string_v else str(self.data[key])
        else: return self.data if not string_v else {k: str(self.data[k]) for k in self.data}

    # percent difference from mean
    def update_mean_delta(self, mean):
        if self.portfolio.get_is_trade_ready() and mean:
            self.data['portfolio_mean'] = mean #probably should be in portfolio class, but this is convenient
            self.data['mean_delta'] = calculate_delta(mean, self.data['cash_value'])

    # when ticker info comes in, check percent difference from mean, buy or sell if outside threshold
    def check_threshold(self):
        if self.portfolio.get_is_trade_ready() and not self.portfolio.seed:
            if self.data.get('mean_delta'):
                if (self.data['mean_delta'] >= self.threshold
                    and self.portfolio.wait_until < time.time()):
                    self._sell()
                if (self.data['mean_delta'] <= self.threshold * -1 #threshold is low
                    and self.portfolio.wait_until < time.time()): #no requests out
                    self._buy()     

    # called from portfolio when starting with nothing
    def seed(self):
        price = self._get_sell_price()
        size = self._get_seed_size(price)
        if Decimal(self.data['balance']) == Decimal(0):
            self.client.place_order(product_id=self.data['product_id'], 
                                size=size, price=price, side='buy')

    # some data cleansing
    def _init_data(self, data, account):
        data['product_id'] = data['id']
        data['id'] = data['id'].replace('-USD', '')
        data['account_id'] = account['id']
        data['balance'] = account['balance']
        data['cash_value'] = Decimal(0)
        data['cash_value_s'] = '0.0'
        self.data = data

    # calculates real time value from ticker price
    def _set_cash_value(self):
        if self.portfolio.get_is_trade_ready():
            self.data['cash_value'] = Decimal(self.data['price']) * Decimal(self.data['balance'])
            self.data['cash_value_s'] = str(self.data['cash_value'])

    def _get_sell_price(self):
        price = Decimal(self.data['best_ask']) - Decimal(self.data['quote_increment'])
        return self._round_price(price)

    def _get_sell_size(self, price):
        amount_over_mean = Decimal(self.data['cash_value']) - Decimal(self.data['portfolio_mean'])
        return self._round_size(amount_over_mean / Decimal(price))

    def _get_buy_price(self):
        price = Decimal(self.data['best_bid']) + Decimal(self.data['quote_increment'])
        return self._round_price(price)

    def _get_buy_size(self, price):
        amount_under_mean = Decimal(self.data['portfolio_mean']) - Decimal(self.data['cash_value'])
        return self._round_size(amount_under_mean / Decimal(price))

    def _get_seed_size(self, price):
        amount_under_mean = (Decimal(self.portfolio.portfolio_balance) / len(self.portfolio.products)) - Decimal(self.data['cash_value'])
        return self._round_size(amount_under_mean / Decimal(price))

    #price is string, convert to decimal for rounding, return as string for api
    def _round_price(self, price):
        decimal_places = len(self.data['quote_increment'].split('.')[1])
        return str(round(Decimal(price), decimal_places))

    #size is string, convert to decimal for rounding, return as string for api
    def _round_size(self, size):
        if '.' in self.data['base_increment']: #not a whole number
            decimal_places = len(self.data['base_increment'].split('.')[1])
            return str(round(Decimal(size), decimal_places))
        else: return str(round(Decimal(size)))

    def _is_base_min(self, size):
        return Decimal(self.data['base_min_size']) <= Decimal(size)

    def _buy(self, minimum=False):
        price = self._get_buy_price()
        size = self._get_buy_size(price)
        size = size if self._is_base_min(size) and not minimum else self.data['base_min_size']
        self.client.place_order(product_id=self.data['product_id'], 
                                size=size, price=price, side='buy')
        self.portfolio.set_wait_until(time.time() + 61)

    def _sell(self):
        price = self._get_sell_price()
        size = self._get_sell_size(price)
        size = size if self._is_base_min(size) else self.data['base_min_size']
        self.client.place_order(product_id=self.data['product_id'], 
                                size=size, price=price, side='sell')
        self.portfolio.set_wait_until(time.time() + 61)



