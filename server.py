import websockets
import asyncio
import sys
from class_file import *

async def recvfile(websocket, path):
    filename = await websocket.recv()
    mode = await websocket.recv()
    f = File(filename)
    f.write(mode)

start_server = websockets.serve(recvfile, "localhost", 8000)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()