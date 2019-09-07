import asyncio
import websockets


async def send_message():
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        name = "scale up"
        await websocket.send(name)


async def up_server(websocket, path):
    print("receiving...")
    data = await websocket.recv()
    print(data)
    await asyncio.sleep(3)
    await send_message()


loop = asyncio.get_event_loop()
asyncio.ensure_future(websockets.serve(up_server, "localhost", 8544))
pending = asyncio.Task.all_tasks() #allow end the last task!
loop.run_until_complete(asyncio.gather(*pending))
loop.run_forever()

#asyncio.get_event_loop().run_until_complete(hello())