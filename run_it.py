from client import Client
from web_socket import Websocket
from config import excluded_products
from product import Product
from portfolio import Portfolio
import time
import websockets
import functools
import asyncio
import json

def main():
    client = Client()
    accounts = client.get_accounts()
    products = [Product(x, client, accounts[x['base_currency']]) 
                for x in client.get_products(quote_currency='USD') 
                if x['id'] not in excluded_products]
    portfolio = Portfolio(products, accounts['USD'], client)


    #incoming websocket from coinbase
    websocket = Websocket(products, portfolio, client.get_user_id())
    websocket.start()
    # websocket to serve react client
    start_server = websockets.serve(functools.partial(handler, portfolio=portfolio), "127.0.0.1", 8888)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()


async def handler(websocket, path, portfolio):
    while True:
        await websocket.send(json.dumps(portfolio.get_websocket_data()))
        await asyncio.sleep(1)



if __name__ == "__main__":
    main()