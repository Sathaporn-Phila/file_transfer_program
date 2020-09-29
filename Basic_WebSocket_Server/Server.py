import websockets
import asyncio

async def hello(websocket, path):
    message = await websocket.recv() # receive message from client
    print(message)
    greeting = f"This message is from server. It receive message from you. It is {message}"
    await websocket.send(greeting) # send message back to client

start_server = websockets.serve(hello, "localhost", 8000)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()