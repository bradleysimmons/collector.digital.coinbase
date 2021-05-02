    # websocket to serve react client
    start_server = websockets.serve(functools.partial(outgoing_handler, portfolio=portfolio), "127.0.0.1", 8888)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()


async def outgoing_handler(websocket, path, portfolio):
    while True:
        await websocket.send(json.dumps(portfolio.get_websocket_data()))
        await asyncio.sleep(1)