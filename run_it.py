from client import Client
from websocket_client import WebsocketClient
from websocket_server import WebsocketServer
from config import excluded_products, included_products
from product import Product
from portfolio import Portfolio
import time
import websockets
import functools
import asyncio
import json
import argparse
import websocket_client

# pass seed to distribute cash across products
parser = argparse.ArgumentParser()
parser.add_argument('--seed', action='store_true')
args = parser.parse_args()

def main():
    client = Client()  # for interacting with coinbase api
    user_id = client.get_user_id()
    accounts = client.get_accounts() # get existing balances

    product_ids = [x for x in client.get_products(quote_currency='USD') 
                    if x['id'] in included_products] # instantiate some products based on included_products list
    portfolio = Portfolio(product_ids, accounts, client, args.seed, user_id) # portfolio is for collection level attributes / behavior
    
    # incoming websocket from coinbase
    coinbase_websocket = WebsocketClient(portfolio)
    # outgoing websocket to web client
    webclient_websocket = WebsocketServer(portfolio)

    asyncio.run(run_websockets(coinbase_websocket, webclient_websocket))

async def run_websockets(coinbase_websocket, webclient_websocket):
    await asyncio.gather(coinbase_websocket.init_websocket(), webclient_websocket.serve_websocket())


if __name__ == "__main__":
    main()