import asyncio
import websockets
import json

class File:
    
    def __init__(self, filename):
        self.filename = filename
    
    def read(self):
        f = open(r"{}".format(self.filename), 'r')
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
        f = open(r"{}".format(self.filename), 'r')
        for line in f:
            await conn.send(line)
        f.close()
    
    async def write(self):
        f = open(r"{}".format(self.filename), 'x')
        line = await conn.recv()
        while line:
            f.write(line)
            line = await conn.recv()
        f.close()
    
    def check(self):
        f = open(r"{}".format(self.filename), 'r')
        line_size = []
        for line in f:
            size = len(line)
            line_size.append(size)
        f.close()
        line_size_json = json.dumps(line_size)
        return line_size_json