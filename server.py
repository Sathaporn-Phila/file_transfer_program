import websockets
import asyncio
import sys
import datetime
import json
from class_file import *
from file_database import *

class Server(object):
    
    def __init__(self, addr, port):
        self.address = addr
        self.port = port
        self.db = File_database()
        self.client_dict = {}
        self.start_server = websockets.serve(self.recvfile, self.address, self.port)
        asyncio.get_event_loop().run_until_complete(self.start_server)
        asyncio.get_event_loop().run_forever()

    async def recvfile(self, websocket, path):
        print("Now connecting with database.")
        while True:
            comm = await websocket.recv()
            if comm == 'login':
                await asyncio.sleep(1)
                print(f"Client {websocket} : request to login.")
                login_username = await websocket.recv()
                print(f"Username : {login_username}")
                await asyncio.sleep(1)
                login_password = await websocket.recv()
                print(f"Password : {login_password}")
                await asyncio.sleep(1)
                confirm = self.db.login(login_username, login_password)
                print(confirm)
                if confirm == "pass":
                    await asyncio.sleep(1)
                    await websocket.send(confirm)
                    self.client_dict[websocket] = [login_username, login_password]
                print(f"Client {websocket} : login complete.")
            
            elif comm == 'register':
                await asyncio.sleep(1)
                print(f"Client {websocket} : request to register.")
                register_username = await websocket.recv()
                await asyncio.sleep(1)
                print(f"Username : {register_username}")
                register_password = await websocket.recv()
                print(f"Password : {register_password}")
                await asyncio.sleep(1)
                self.db.register_account(register_username, register_password)
                print(f"Client {websocket} : register complete.")

            elif comm == 'send_direct':
                await asyncio.sleep(1)
                json_file_data = await websocket.recv()
                file_data = json.loads(json_file_data)
                await self.write(websocket, file_data[3])
                self.db.add_inbox(file_data[0],file_data[1],file_data[3],'wait for data?',file_data[4],file_data[2])
            
            elif comm == 'send_public':
                await asyncio.sleep(1)
                json_file_data = await websocket.recv()
                file_data = json.loads(json_file_data)
                print(file_data)
                print(file_data[3])
                await self.write(websocket, file_data[3])
                self.db.add_public(file_data[0],file_data[1],file_data[3],'wait for data?',file_data[4])

            elif comm == 'checkfile':
                await asyncio.sleep(1)
                dest_file_size = self.check(file_data[4])
                await asyncio.sleep(1)
                client_file_size_json = await websocket.recv()
                client_file_size = json.loads(client_file_size_json)
                if dest_file_size == client_file_size:
                    file_check_status = "complete"
                else:
                    file_check_status = "incomplete"
                await asyncio.sleep(1)
                await websocket.send(file_check_status)

            elif comm == "browse_inbox":
                inbox = self.db.get_inbox()
                await asyncio.sleep(1)
                await websocket.send(inbox)

            elif comm == "browse_public":
                public = self.db.get_public()
                await asyncio.sleep(1)
                await websocket.send(public)

            elif comm == "browse_history":
                history = self.db.get_send_history()
                await asyncio.sleep(1)
                await websocket.send(history)
            
            elif comm == "find_user":
                user = await websocket.recv()
                status = self.db.search_name(user)
                await websocket.send(status)

            else:
                continue
                # await asyncio.sleep(1)
                # jsonlist = await websocket.recv()
                # await asyncio.sleep(1)
                # rawlist = json.loads(jsonlist)

    def check(self, filename):
        f = open(r"{}".format(filename), 'r')
        line_size = []
        for line in f:
            size = len(line)
            line_size.append(size)
        f.close()
        return line_size
    
    async def write(self, conn, filepath, default="D:\\vs_studio\\sdp_project\\file_transfer_program\\saved\\"):
        filename = filepath
        f = open(r"{}{}".format(default, filepath), 'w')
        jsonline = await conn.recv()
        line = json.loads(jsonline)
        while line != "":
            print(line)
            await asyncio.sleep(1)
            f.write(line)
            jsonline = await conn.recv()
            line = json.loads(jsonline)
        f.close()

if __name__ == '__main__':
    Server("localhost", "8000")