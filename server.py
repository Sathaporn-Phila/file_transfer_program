import websockets
import asyncio
import sys
from class_file import *
from file_database import *

db = File_database()
print("Now connecting with database.")
client_dict = {}
async def recvfile(websocket, path):
    while True:
        comm = await websocket.recv()
        if comm == 'login':
            client_data = await websocket.recv()
            db.login(client_data[0], client_data[1])
            client_dict[[client_data[0], client_data[1]]] = websocket
        
        elif comm == 'register':
            client_data = await websocket.recv()
            db.register_account(client_data[0], client_data[1])

        elif comm == 'send_direct':
            file_data = await websocket.recv()
            f = File(file_data[4])
            f.write()
            db.add_inbox(file_data[3],file_data[0],file_data[1],file_data[4],'wait for data?','file_type')
        
        elif comm == 'send_public':
            file_data = await websocket.recv()
            f = File(file_data[4])
            f.write()
            db.add_public(file_data[0],file_data[1],file_data[4],'wait for data?','file_type')

        elif comm == 'checkfile':
            dest_file_size = f.check()
            client_file_size = await websocket.recv()
            if dest_file_size == client_file_size:
                file_check_status = "complete"
            else:
                file_check_status = "incomplete"
            await websocket.send(file_check_status)

start_server = websockets.serve(recvfile, "localhost", 8000)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()