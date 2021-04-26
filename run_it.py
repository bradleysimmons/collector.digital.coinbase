from client import Client
from web_socket import Websocket
from config import excluded_products, threshold, included_products
from product import Product
from portfolio import Portfolio
import time
import websockets
import functools
import asyncio
import json
import argparse

# pass seed to distribute cash across products
parser = argparse.ArgumentParser()
parser.add_argument('--seed', action='store_true')
args = parser.parse_args()

def main():
    client = Client()  # for interacting with coinbase api
    accounts = client.get_accounts() # get existing balances
    products = [Product(x, client, accounts[x['base_currency']], threshold) 
                for x in client.get_products(quote_currency='USD') 
                if x['id'] in included_products] # instantiate some products based on included_products list
    portfolio = Portfolio(products, accounts['USD'], client, args.seed) # portfolio is for collection level attributes / behavior
    for product in products: product.portfolio = portfolio # passed it back down to get some attributes on the product level
                                                           # could have done this more smoothly

    # incoming websocket from coinbase
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