import websockets
import asyncio

async def hello(websocket, path):
    message = await websocket.recv()
    greeting = f"This message is from server. It receive message from you. It is '{message}'"
    await websocket.send(greeting)

start_server = websockets.serve(hello, "localhost", 8000)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()