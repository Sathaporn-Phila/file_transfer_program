import websockets
import asyncio
import sys
import json
from class_file import *

class Client(object):
    
    class FTP(object):
        
        def __init__(self, addr, port):
            self.address = addr
            self.port = port
            self.uri = f"ws://{self.address}:{self.port}"

        async def main(self):
            conn = await websockets.connect(self.uri)
            self.conn = conn
            while True:
                comm = input("Enter your command : [Register, Login, Send a file, Browse]\n")
                if comm == "Register":
                    await self.conn.send("register")
                    register_username = str(input("Username : "))
                    await self.conn.send(register_username)
                    register_password = str(input("Password : "))
                    await self.conn.send(register_password)
                elif comm == "Login":
                    check_login = True
                    while check_login:
                        await self.conn.send("login")
                        login_username = input("Username : ")
                        await self.conn.send(login_username)
                        login_password = input("Password : ")
                        await self.conn.send(login_password)
                        login_status = await self.conn.recv()
                        if login_status == "pass":
                            check_login = not check_login
                    self.username = login_username
                elif comm == "Send a file":
                    file_path = self.test_open()
                    title = input("Write your title : ")
                    author = self.username
                    filename, fileextension = self.custom_path(file_path)
                    send_mode = self.find_sendmode()
                    file_data = [title, author, dest_user, filename, fileextension]
                    await self.conn.send(send_mode)
                    await self.conn.send(file_data)
                    f = File(file_path)
                    f.send()
                    self.checksenderfile()
                elif comm == "Browse":
                    browse_comm = self.find_browse()
                    await self.conn.send(browse_comm)
                    inbox_list = await self.conn.recv()
                    for line in inbox_list:
                        print(line)
                else:
                    print("Command not in the list.")
                    continue

        def test_open(self):
            file_path = input("Enter your file path : ")
            try:
                f = open(filepath, "r")
                return file_path
            except:
                print("Can't find a file.")
                return self.test_open()
        
        async def find_user(self):
            dest_user = input("Who you want to send to (Username) : ")
            confirm = await self.conn.send("find user")
            if confirm:
                return dest_user
            else:
                self.find_user()
        
        def find_sendmode(self):
            file_comm = input("Public or Private : ")
            if file_comm == "Private":
                dest_user = self.find_user()
                return "send_direct"
            elif file_comm == "Public":
                return "send_public"
            else:
                find_sendmode()
        
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
        
        def custom_path(self,filepath):
            filename_index = -1
            while filepath[filename_index] != "\\":
                fliename_index -= 1
            filename = filepath[filename_index:]
            fileextension_index = -1
            while file_path[fileextension_index] != ".":
                fileextension_index -= 1
            fileextension = file_path[fileextension_index:]
            return filename, fileextension

        async def checksenderfile(self):
            file_size = f.check()
            await self.conn.send("checkfile")
            await self.conn.send(file_size)
            confirm_status = await self.conn.recv()
            if confirm_status == "complete":
                print("File completly send")
            else:
                print("File incompletely send")
    
    def __init__(self, addr='localhost', port='8000'):
        self.func = self.FTP(addr, port)
    
    def start(self):
        asyncio.get_event_loop().run_until_complete(self.func.main())

if __name__ == "__main__":
    c = Client()
    c.start()