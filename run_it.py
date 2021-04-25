
from client import Client
from web_socket import Websocket
from config import excluded_products
from product import Product
import time

def main():
    client = Client()
    products = [Product(x) for x in client.get_products(quote_currency='USD') if x['id'] not in excluded_products]
    websocket = None

    try:
        while True:
            if not websocket or websocket.error: 
                websocket = Websocket(products, client.get_user_id())
                websocket.start()
            time.sleep(1)
    except KeyboardInterrupt:
        websocket.close()

if __name__ == "__main__":
    main()