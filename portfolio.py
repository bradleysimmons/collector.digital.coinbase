from product import Product
from decimal import Decimal
import time
from config import threshold
from helpers import calculate_delta

class Portfolio():
    def __init__(self, products, client):
        self.is_trade_ready = False
        self.user_id = client.get_user_id()
        self.accounts = client.get_accounts() # get existing balances
        self.fee_rate = Decimal(client.get_taker_fee_rate())
        self.usd_account_id = self.accounts['USD']['id']
        self.products = [Product(x, client, self.accounts[x['base_currency']], threshold, self) for x in products]
        self.products_dict = {product.product_id: product for product in self.products}
        self.cash_balance = Decimal(self.accounts['USD']['balance'])
        self.client = client
        self.wait_until = time.time()
        self.portfolio_balance = None
        self.target_mean = None
        self.threshold = threshold
        self.balancing = False
        #
        self.opening_portfolio_balance = None
        self.market_delta = None
        self.balance_delta = None

        
    # to send out to react client
    def get_websocket_data(self):
        return {
            'products': [x.get_data() for x in self.products],
            'portfolio': {'portfolio_balance': str(self.portfolio_balance),
                            'cash_balance': str(self.cash_balance),
                            'market_delta': str(self.market_delta),
                            'balance_delta': str(self.balance_delta),
                            'balancing': self._get_balancing()}
        }

    def _set_portfolio_balance(self):
        if self.get_is_trade_ready():
            self.portfolio_balance = sum(x.cash_value for x in self.products) + self.cash_balance

    def _set_cash_balance(self):
        self.cash_balance = Decimal(self.client.get_balance(self.usd_account_id))

    def _set_target_mean(self):
        if self.portfolio_balance:
            self.target_mean = self.portfolio_balance / len(self.products)

    def _set_market_delta(self):
        if self.get_is_trade_ready():
            self.market_delta = sum(x.market_delta for x in self.products) / len(self.products)

    def _set_balance_delta(self):
        if self.portfolio_balance:
            self.balance_delta = calculate_delta(self.opening_portfolio_balance, self.portfolio_balance)

    def _is_over_threshold(self):
        if not all([x.mean_diff for x in self.products]): return None
        return any([abs(x.mean_diff) > threshold for x in self.products])

    def _has_been_balanced(self):
        return all([x.trade_counter or x.is_within_min_cost_of_mean() for x in self.products])

    def _get_balancing(self):
        return self.balancing

    def _set_balancing(self, value):
        self.balancing = value

    # set the wait until value so only one order is out at time, based off 1 min limit orders
    def set_wait_until(self, value):
        self.wait_until = value

    # safety to make sure every product has a price before stuff happens
    def get_is_trade_ready(self):
        if self.is_trade_ready == True: return True
        if all([x.price for x in self.products]):
            self.is_trade_ready = True
            self.opening_portfolio_balance = sum(x.cash_value for x in self.products) + self.cash_balance
            return True
        return False

    def handle_ticker_message(self, message):
        if message['type'] in ['ticker']:
            self.products_dict[message['product_id']].update_data(message)
            self._set_portfolio_balance()
            self._set_target_mean()
            self._set_market_delta()
            self._set_balance_delta()
            self.products_dict[message['product_id']].update_mean_diff()
            if self._is_over_threshold() and not self._has_been_balanced():
                self.balancing = True
            if self.balancing and self._has_been_balanced():
                self.balancing = False
                for product in self.products: product.set_trade_counter(0)
            self.products_dict[message['product_id']].handle_balancing()

        if message.get('user_id') == self.user_id and message['type'] == 'done':
            self.products_dict[message['product_id']].set_trade_counter(1)
            self.products_dict[message['product_id']].set_balance()
            self._set_cash_balance()
            self.products_dict[message['product_id']].set_wait_until(time.time())  





