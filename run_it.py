
from client import Client
from web_socket import Websocket
from config import excluded_products
import time

def main():
    client = Client()
    products = [x for x in client.get_products(quote_currency='USD') if x not in excluded_products]
    websocket = Websocket(products=[x['id'] for x in products], user_id=client.get_user_id())
    websocket.start()
    try:
        while True:
            time.sleep(1)
        
    except KeyboardInterrupt:
        websocket.close()
    


if __name__ == "__main__":
    main()