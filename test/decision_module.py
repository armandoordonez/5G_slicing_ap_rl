import asyncio
import websockets
import json
import datetime
#import rl_module
#todo implement interface/abstract method
class decision_module():
    def __init__(self):
        self.vnfid_timestamps = {}
        #rl_module = module()
        self.start()
        
    def start(self):
        loop = asyncio.get_event_loop()
        asyncio.ensure_future(websockets.serve(self.train_server, "localhost", 8544))
        pending = asyncio.Task.all_tasks() #allow end the last task!
        loop.run_until_complete(asyncio.gather(*pending))
        loop.run_forever()


    async def send_message(self, message):
        uri = "ws://localhost:8765"
        async with websockets.connect(uri) as websocket:
            await websocket.send(json.dumps(message))


    async def train_server(self, websocket, path):
        print("receiving...")
        data = await websocket.recv()
        vnf_json_data = json.loads(data)
        print(vnf_json_data)



        
        print(vnf_json_data["vnf_id"])
        print(self.vnfid_timestamps.keys())
        if not vnf_json_data["vnf_id"] in self.vnfid_timestamps.keys():
            print("first time")
            self.vnfid_timestamps[vnf_json_data["vnf_id"]] = datetime.datetime.now()
            message = await self.scale_decision(vnf_json_data)
            await self.send_message(message)    
    
        elif(((datetime.datetime.now() - self.vnfid_timestamps[vnf_json_data["vnf_id"]]).total_seconds() / 60.0) > 1): 
            print("1 minute pass already... sending new order to scale....")
            message = await self.scale_decision(vnf_json_data)
            await self.send_message(message)
            self.vnfid_timestamps[vnf_json_data["vnf_id"]] = datetime.datetime.now()   
        else:
            print("discarting message...")
        #rl_module.train(data)
        
        #message = await self.scale_decision("json")
        await self.send_message(vnf_json_data)
    
    async def inference_server(self, websocket, path):
        
        pass

    async def scale_decision(self, message):
        await asyncio.sleep(3) 
        message["flavor"] = "double"
        message["volume"] = "medium"
        return message
        
#    async def scale_module(self, cpu, docker_id, ns_id, vnf_id, flavor_type, current_instance_number):
#        pass

if __name__ == "__main__":
    decision_module()