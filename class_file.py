import asyncio
import websockets

class File:
    
    def __init__(self, filename):
        self.filename = filename
    
    def read(self):
        f = open(self.filename, 'r')
        for line in f:
            print(line)
        f.close()
    
    def readbinary(self):
        f = open(self.filename, 'rb')
        r = f.read(1024)
        while r:
            print(r)
            r = f.read(1024)

    async def send(self):
        f = open(self.filename, 'r')
        for line in f:
            await websocket.send(line)
        f.close()
    
    async def write(self):
        f = open(self.filename, 'w')
        line = await websocket.recv()
        while line:
            f.write(line)
            line = await websocket.recv()
        f.close()
    
    def check(self):
        f = open(self.filename, 'r')
        line_size = []
        for line in f:
            size = len(line)
            line_size.append(size)
        f.close()
        return line_size