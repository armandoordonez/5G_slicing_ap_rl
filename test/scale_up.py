import asyncio
import websockets
import json
import datetime
import keys as keys
#import rl_module
#todo implement interface/abstract method
class decision_module():
    scale_up_message = {
                    keys.flavor: "single", 
                    keys.volume: "small",
                    keys.ns_id: "3ef4dfc2-ac73-4171-938f-4fddcce3fec3",
                    keys.vnf_id: "34ae306c-2fba-45ef-97ed-bbf77ca5528e",
                    keys.vnf_index: "2",
                    keys.sampling_time: 5,
                    keys.scale_decision: "scale_down"
                }
    def __init__(self):
        self.vnfid_timestamps = {}
        #rl_module = module()
        self.start()
        
    def start(self):
        loop = asyncio.get_event_loop()
        asyncio.ensure_future(self.send_message(self.scale_up_message))
        #asyncio.ensure_future(websockets.serve(self.train_server, "localhost", 8544))
        pending = asyncio.Task.all_tasks() #allow end the last task!
        loop.run_until_complete(asyncio.gather(*pending))
        loop.run_forever()


    async def send_message(self, message):
        uri = "ws://localhost:8765"
        async with websockets.connect(uri) as websocket:
            await websocket.send(json.dumps(message))
        
#    async def scale_module(self, cpu, docker_id, ns_id, vnf_id, flavor_type, current_instance_number):
#        pass

if __name__ == "__main__":
    decision_module()