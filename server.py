import websockets
import asyncio
import sys
from class_file import *
from file_database import *

db = File_database()
print("Now connecting with database.")
client_dict = {}
async def recvfile(websocket, path):
    client_username = await websocket.recv()
    client_password = await websocket.recv()
    db.login(client_username, client_password)
    client_dict[[client_username, client_password]] = websocket
    while True:
        comm = await websocket.recv()
        if comm == 'send_direct':
            file_data = await websocket.recv()
            f = File(file_data[2])
            f.write()
            db.add_inbox(file_data[0],file_data[1],file_data[2],file_data[3],file_data[4],file_data[5])
        elif comm == 'send_public':
            filename = await websocket.recv()
            f = File(filename)
            f.write()
start_server = websockets.serve(recvfile, "localhost", 8000)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
