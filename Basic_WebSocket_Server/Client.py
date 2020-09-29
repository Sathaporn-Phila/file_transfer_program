import websockets
import asyncio

async def hello():
    uri = "ws://localhost:8000"
    async with websockets.connect(uri) as websocket:
        print("You are now connecting with a server.")
        message = input(">>>")
        await websocket.send(message)
        response = await websocket.recv()
        print(response)

asyncio.get_event_loop().run_until_complete(hello())