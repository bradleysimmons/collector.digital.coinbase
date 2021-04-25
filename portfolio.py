

class Portfolio():
    def __init__(self, products, usd_account, client):
        self.products = products
        self.cash_balance = usd_account['balance']
        self.usd_account_id = usd_account['id']
        self.client = client
        self.set_cash_value()

    def get_websocket_data(self):
        return {
            'products': [x.get_data(string_v=True) for x in self.products],
            'portfolio': {'cash_value': str(self.cash_value),
                            'cash_balance': self.cash_balance}
        }

    def set_cash_value(self):
        self.cash_value = sum(x.get_data(key='cash_value') for x in self.products)

    def set_cash_balance(self):
        self.cash_balance = self.client.get_balance(self.usd_account_id)