import websockets
import asyncio

async def recvfile(websocket, path):
    filename = await websocket.recv()
    mode = await websocket.recv()
    f = open(filename, mode)
    line = await websocket.recv()
    while line:
        f.write(line)
        line = await websocket.recv()
    f.close()

start_server = websockets.serve(recvfile, "localhost", 8000)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
