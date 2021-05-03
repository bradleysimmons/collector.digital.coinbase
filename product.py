from decimal import Decimal
from helpers import calculate_delta
import time

class Product():
    def __init__(self, data, client, account, threshold, portfolio):
        self.product_id = data['id']
        self.base_currency = data['base_currency']
        self.base_min_size = Decimal(data['base_min_size'])
        self.quote_increment = Decimal(data['quote_increment'])
        self.base_increment = data['base_increment']
        self.account_id = account['id']
        self.balance = Decimal(account['balance'])
        self.threshold = threshold #percent on which to act
        self.mean_diff = None #difference from portfolio mean value
        self.cash_value = None #price * size
        self.price = None
        self.open_24h = None
        self.low_24h = None
        self.high_24h = None
        self.best_bid = None
        self.best_ask = None
        self.client = client #for api calls
        self.portfolio = portfolio #to get to the collection level attributes/actions
        self.wait_until = time.time()

    def update_data(self, data):
        self.price = Decimal(data['price'])
        self.open_24h = Decimal(data['open_24h'])
        self.low_24h = Decimal(data['low_24h'])
        self.high_24h = Decimal(data['high_24h'])
        self.best_bid = Decimal(data['best_bid'])
        self.best_ask = Decimal(data['best_ask'])
        self._set_cash_value() # calculation based on price
        self._set_trade_minimum()

     # calculates real time value from ticker price
    def _set_cash_value(self):
        self.cash_value = self.price * self.balance

    # when a trade is confirmed
    def set_balance(self):
        self.balance = Decimal(self.client.get_balance(self.account_id))

    def get_data(self):
        keys = ['product_id', 'cash_value', 'price', 'balance', 'mean_diff', 'base_currency']
        return {k: str(getattr(self, k)) for k in keys}

    # percent difference from mean
    def update_mean_diff(self):
        if self.portfolio.get_is_trade_ready():
            self.mean_diff = calculate_delta(self.portfolio.target_mean, self.cash_value)

    def is_within_min_cost_of_mean(self):
        return abs(self.portfolio.target_mean - self.cash_value) < self.trade_minimum

    def handle_balancing(self):
        if self.portfolio.balancing and not self.is_within_min_cost_of_mean():
            if self._need_to_buy_some() and self.wait_until < time.time():
                self._buy()
            if self._need_to_sell_some() and self.wait_until < time.time():
                self._sell()

    def _need_to_buy_some(self):
        return self.cash_value < self.portfolio.target_mean

    def _need_to_sell_some(self):
        return self.cash_value > self.portfolio.target_mean

    def _set_trade_minimum(self):
        self.trade_minimum = self.base_min_size * self.price

    def _get_sell_price(self):
        price = self.best_ask - self.quote_increment
        return self._round_price(price)

    def _get_sell_size(self, price):
        amount_over_mean = self.cash_value - self.portfolio.target_mean
        return self._round_size(amount_over_mean / price, sell=True)

    def _get_buy_price(self):
        price = self.best_bid + self.quote_increment
        return self._round_price(price)

    def _get_buy_size(self, price):
        amount_under_mean = self.portfolio.target_mean - self.cash_value
        if amount_under_mean > self.portfolio.cash_balance: #in case some of them have moved a bit
            return self._round_size(self.portfolio.cash_balance / price, buy=True)
        else: return self._round_size(amount_under_mean / price, buy=True)

    #price is string, convert to decimal for rounding, return as string for api
    def _round_price(self, price):
        decimal_places = len(str(self.quote_increment).split('.')[1])
        return round(Decimal(price), decimal_places)

    def _round_size(self, size, buy=False, sell=False):
        if sell: size = size + (size * self.portfolio.fee_rate)
        if buy: size = size - (size * self.portfolio.fee_rate)
        if '.' in self.base_increment: #not a whole number
            decimal_places = len(self.base_increment.split('.')[1])
            return round(size, decimal_places)
        else: return round(size)

    def set_wait_until(self, value):
        self.wait_until = value

    def _buy(self, minimum=False):
        price = self._get_buy_price()
        size = self._get_buy_size(price)
        print(self.product_id)
        print('buy')
        print(size)
        print(price)
        self.client.place_order(product_id=self.product_id, 
                                size=size, price=price, side='buy')
        self.set_wait_until(time.time() + 61)

    def _sell(self):
        price = self._get_sell_price()
        size = self._get_sell_size(price)
        print(self.product_id)
        print('sell')
        print(size)
        print(price)
        self.client.place_order(product_id=self.product_id, 
                                size=size, price=price, side='sell')
        self.set_wait_until(time.time() + 61)



