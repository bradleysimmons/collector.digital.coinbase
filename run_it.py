from client import Client
from web_socket import Websocket
from config import excluded_products
from product import Product
import time
import websockets
import functools
import asyncio
import json

def main():
    client = Client()
    products = [Product(x) for x in client.get_products(quote_currency='USD') if x['id'] not in excluded_products]
    websocket = Websocket(products, client.get_user_id())
    websocket.start()
    # websocket to serve react client
    start_server = websockets.serve(functools.partial(handler, products=products), "127.0.0.1", 8888)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()


async def handler(websocket, path, products):
    while True:
        await websocket.send(json.dumps([x.get_data() for x in products]))
        await asyncio.sleep(1)

if __name__ == "__main__":
    main()