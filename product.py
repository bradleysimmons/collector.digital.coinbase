class Product():
    def __init__(self, data):
        self.data = data

    def update_data(self, data):
        self.data.update(data)
        print(self.data)