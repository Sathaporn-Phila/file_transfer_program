import websockets
import asyncio
import sys
from class_file import *
from file_database import *

class Server(object):
    
    def __init__(self, addr, port):
        self.address = addr
        self.port = port
        self.db = File_database()
        print("Now connecting with database.")
        self.client_dict = {}
        self.start_server = websockets.serve(self.recvfile, self.address, self.port)
        asyncio.get_event_loop().run_until_complete(self.start_server)
        asyncio.get_event_loop().run_forever()

    async def recvfile(self,websocket, path):
        while True:
            comm = await websocket.recv()
            if comm == 'login':
                client_data = await websocket.recv()
                self.db.login(client_data[0], client_data[1])
                self.client_dict[[client_data[0], client_data[1]]] = websocket
            
            elif comm == 'register':
                client_data = await websocket.recv()
                self.db.register_account(client_data[0], client_data[1])

            elif comm == 'send_direct':
                file_data = await websocket.recv()
                f = File(file_data[4])
                f.write()
                self.db.add_inbox(file_data[3],file_data[0],file_data[1],file_data[4],'wait for data?','file_type')
            
            elif comm == 'send_public':
                file_data = await websocket.recv()
                f = File(file_data[4])
                f.write()
                self.db.add_public(file_data[0],file_data[1],file_data[4],'wait for data?','file_type')

            elif comm == 'checkfile':
                dest_file_size = f.check()
                client_file_size = await websocket.recv()
                if dest_file_size == client_file_size:
                    file_check_status = "complete"
                else:
                    file_check_status = "incomplete"
                await websocket.send(file_check_status)