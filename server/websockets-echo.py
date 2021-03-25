#!/usr/bin/env python3

# WS server that sends messages at random intervals

import asyncio
import datetime
import random
import websockets

async def time(websocket, path):
    await websocket.send('Hello')
    while True:
        r = await websocket.recv()
        await websocket.send(r)

start_server = websockets.serve(time, "127.0.0.1", 5678)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
