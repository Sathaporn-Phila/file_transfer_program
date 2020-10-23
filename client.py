import websockets
import asyncio
import sys
from class_file import *

class Client(object):
    
    class FTP(object):
        
        def __init__(self, addr, port):
            self.address = addr
            self.port = port
            self.uri = f"ws://{self.address}:{self.port}"

        async def start(self):
            conn = await websockets.connect(self.uri)
            self.conn = conn
            await self.conn.send("FUCK U")

        async def login(self, username, password):
            await self.conn.send(username)
            await self.conn.send(password)
            login_status = await self.conn.recv()
            if login_status:
                self.username = username
                self.password = password

        async def sendfile(self, title, author, mode, filename, newfilename, dest=""):
            while True:
                try:
                    f = open(filename, "r")
                    f.close()
                    break
                except:
                    continue
            self.conn.send(mode)
            f = File(filename)
            file_data = [title, author, mode, dest, newfilename]
            await self.conn.send(file_data)
            f.send()
            self.checksenderfile()

        async def checksenderfile(self):
            file_size = f.check()
            await self.conn.send("checkfile")
            await self.conn.send(file_size)
            confirm_status = await self.conn.recv()
            if confirm_status == "complete":
                print("file completly send")
            else:
                print("file incompletely send")
    
    def __init__(self, addr='localhost', port='8000'):
        self.func = self.FTP(addr, port)
    
    def do_start(self):
        asyncio.get_event_loop().run_until_complete(self.func.start())
        
    def do_login(self, username, password):
        asyncio.get_event_loop().run_until_complete(self.func.login(username, password))
    
    def do_sendfile(self, title, author, mode, filename, newfilename, dest=""):
        asyncio.get_event_loop().run_until_complete(self.func.sendfile(title, author, mode, filename, newfilename, dest=""))

if __name__ == "__main__":
    c = Client()
    c.do_start()