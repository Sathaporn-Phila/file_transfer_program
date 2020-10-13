import websockets
import asyncio
import sys
from class_file import *

uri = "ws://localhost:8000"
async def sendfile():
    async with websockets.connect(uri) as websocket:
        while True:
            filename = input("Enter your file to send (Full path): ")
            try:
                f = open(filename, "r")
                f.close()
                break
            except:
                continue
        newname = input("Enter your new filename : ")
        f = File(filename)
        await websocket.send(newname)
        while True:
            mode = input("Which mode to read : (r/rb)")
            if mode == "r":
                sendmode = "w"
                break
            elif mode == "rb":
                sendmode = "wb"
                break
            print("Wrong answer pls choose again.")
        await websocket.send(sendmode)
        f.send(mode)
        websocket.close()

async def checksenderfile():
    async with websockets.connect(uri) as websocket:
        await websocket.send(f.check())
        websocket.close()

asyncio.get_event_loop().run_until_complete(sendfile())