import asyncio
import websockets

async def hello(websocket, path):
    message = await websocket.recv()
    print("{message}")
    """
    name = await websocket.recv()
    print(f"< {name}")

    greeting = f"Hello {name}!"

    await websocket.send(greeting)
    print("{greeting}")
    """

start_server = websockets.serve(hello, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()