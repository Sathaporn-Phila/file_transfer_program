import websockets
import asyncio
import sys
from class_file import *

client_dict = {}
async def recvfile(websocket, path):
    while True:
        client_username = await websocket.recv()
        client_dict[client_username] = websocket
        comm = await websocket.recv()
        if comm == 'send_direct':
            filename = await websocket.recv()
            mode = await websocket.recv()
            dest = await websocket.recv()
            recv_line = await websocket.recv()
            while recv_line:
                await client_dict[dest].send(recv_line)
        elif comm == 'send_public':
            filename = await websocket.recv()
            mode = await websocket.recv()
            f = File(filename)
            f.write(mode)
start_server = websockets.serve(recvfile, "localhost", 8000)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
