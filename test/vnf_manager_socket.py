import asyncio 
import websockets
class vnf_manager_prototype(object):
    def __init__(self):
        loop = asyncio.get_event_loop()
        for character in "Anuel":
            asyncio.ensure_future(self.underground_func(character))
        asyncio.ensure_future(websockets.serve(self.hello, "localhost", 8765))
        pending = asyncio.Task.all_tasks() #allow end the last task!
        print(len(pending))
    
        loop.run_until_complete(asyncio.gather(*pending))
        loop.run_forever()

    async def underground_func(self, character):
        counter = 0
        while True:
            await asyncio.sleep(1)
            counter += 1 
            if counter > 3:
                print("emit alert!")
                await self.send_message(character)
                counter = 0
        
    async def hello(self, websocket, path):
        print("waiting...")
        name = await websocket.recv()
        print(name)

    async def send_message(self, message):
        uri = "ws://localhost:8544"
        async with websockets.connect(uri) as websocket:
            await websocket.send(message)
    async def turn_on_server(self, port):
        pass

if __name__ == "__main__":
    vnf_manager_prototype()
