from decimal import Decimal

class Product():
    def __init__(self, data, client, account):
        self._init_data(data, account)
        self.client = client

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
        self.data = data

    def _set_cash_value(self):
        if self.data.get('price') and self.data.get('balance'):
            self.data['cash_value'] = Decimal(self.data['price']) * Decimal(self.data['balance'])
            self.data['cash_value_s'] = str(self.data['cash_value'])

