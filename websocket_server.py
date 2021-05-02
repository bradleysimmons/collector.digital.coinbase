import asyncio
import websockets
import json

class WebsocketServer():
    def __init__(self, portfolio):
        self.portfolio = portfolio

    async def handler(self, websocket, path):
        while True:
            await websocket.send(json.dumps(self.portfolio.get_websocket_data()))
            await asyncio.sleep(.25) 

    async def serve_websocket(self):
        await websockets.serve(self.handler, "127.0.0.1", 8888)