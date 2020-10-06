import websockets
import asyncio

async def sendfile():
    uri = "ws://localhost:8000"
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
        f = open(filename, mode)
        if mode == "r":
            r = f.read()
            while r:
                await websocket.send(r)
                r = f.read()
        else:
            r = f.read(1024)
            while r:
                await websocket.send(r)
                r = f.read(1024)

asyncio.get_event_loop().run_until_complete(sendfile())
