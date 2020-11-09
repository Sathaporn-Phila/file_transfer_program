import websockets
import asyncio
import sys
import json
from class_file import *

class Client():
    def __init__(self, address, port):
        self.address = address
        self.port = port
        self.authorize = False
        self.username = ""
    
    async def start(self):
        asyncio.get_event_loop().run_until_complete(self.main())

    async def main(self):
        self.conn = await websockets.connect(f"ws://{self.address}:{self.port}")        
        while True:
            if self.authorize:
                comm = input("[Send a file, Browse] : ")
                
                if comm == "Send a file":
                    file_path = self.test_open()
                    title = input("Write your title : ")
                    author = self.username
                    filename, fileextension = self.custom_path(file_path)
                    send_mode, dest_user = await self.find_sendmode(self.conn)
                    
                    file_data = [title, author, dest_user, filename, fileextension]
                    file_json = json.dumps(file_data)
                    
                    await conn.send(send_mode)
                    await asyncio.sleep(1)
                    await conn.send(file_json)
                    await asyncio.sleep(1)
                    await self.send(conn, file_path)
                    await asyncio.sleep(1)
                
                elif comm == "Browse":
                    browse_comm = self.find_browse()
                    await asyncio.sleep(1)
                    await conn.send(browse_comm)
                    
                    await asyncio.sleep(1)                    
                    inbox_list = await conn.recv()
                    
                    for line in inbox_list:
                        print(line)
                
                else:
                    continue

            else:
                comm = input("[Login, Register] : ")
                
                if comm == "Register":
                    await asyncio.sleep(1)
                    await conn.send("register")
                    
                    register_username = str(input("Username : "))
                    await asyncio.sleep(1)
                    await conn.send(register_username)
                    
                    register_password = str(input("Password : "))
                    await asyncio.sleep(1)
                    await conn.send(register_password)
                
                elif comm == "Login":
                    while not self.authorize:
                        await asyncio.sleep(1)
                        await conn.send("login")
                        
                        login_username = input("Username : ")
                        await asyncio.sleep(1)
                        await conn.send(login_username)
                        
                        login_password = input("Password : ")
                        await asyncio.sleep(1)
                        await conn.send(login_password)
                        
                        await asyncio.sleep(1)                        
                        login_status = await conn.recv()
                        
                        if login_status == "pass":
                            self.authorize = not self.authorize

                    self.username = login_username
                
                else:
                    continue

    def test_open(self):
        file_path = input("Enter your file path : ")
        try:
            f = open(r"{}".format(file_path), "r")
            return file_path
        except:
            print("Can't find a file.")
            return self.test_open()

    async def find_user(self, conn):
        dest_user = input("Who you want to send to (Username) : ")
        find = await conn.send("find_user")
        await asyncio.sleep(1)
        await conn.send(dest_user)
        await asyncio.sleep(1)
        confirm = await conn.recv()
        if confirm:
            return dest_user
        else:
            await self.find_user(conn)

    async def find_sendmode(self, conn):
        file_comm = input("Public or Private : ")
        if file_comm == "Private":
            dest_user = await self.find_user(conn)
            return "send_direct", dest_user
        elif file_comm == "Public":
            return "send_public", ""
        else:
            await self.find_sendmode(conn)

    def find_browse(self):
        browse = input("Choose what to browse : [inbox, public, sendhistory]\n")
        if browse == "inbox":
            return "browse_inbox"
        elif browse == "public":
            return "browse_public"                        
        elif browse == "sendhistory":
            return "browse_history"
        else:
            return self.find_browse()

    def custom_path(self, filepath):
        filename_index = -1
        while filepath[filename_index] != "\\":
            filename_index -= 1
        filename = filepath[filename_index+1:]
        fileextension_index = -1
        while filepath[fileextension_index] != ".":
            fileextension_index -= 1
        fileextension = filepath[fileextension_index:]
        print(filename, fileextension)
        return filename, fileextension

    async def checksenderfile(self, conn, filepath):
        file_size = self.check(filepath)
        await conn.send("checkfile")
        await asyncio.sleep(1)
        await conn.send(file_size)
        await asyncio.sleep(1)
        confirm_status = await conn.recv()
        if confirm_status == "complete":
            print("File completly send")
        else:
            print("File incompletely send")

    async def send(self, conn, filepath):
        f = open(r"{}".format(filepath), 'r')
        r = f.read()
        while r:
            jsonr = json.dumps(r)
            await conn.send(jsonr)
            await asyncio.sleep(1)
            r = f.read()
        f.close()

    def check(self, filepath):
        f = open(r"{}".format(filepath), 'r')
        line_size = []
        for line in f:
            size = len(line)
            line_size.append(size)
        f.close()
        line_size_json = json.dumps(line_size)
        return line_size_json

if __name__ == "__main__":
    client = Client("localhost", "8000")
    client.start()