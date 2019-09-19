import asyncio
import argparse
import aiohttp
class MultipleRequest():
    def __init__(self, target_ip, target_port):
        self.target_ip = "http://"+target_ip + ":" + target_port
        print("target ip: {}".format(self.target_ip))    
        self.start()


    def start(self):
        print("starting new loop")
        loop = asyncio.get_event_loop()
        for _ in range(55):
            asyncio.ensure_future(self.download(self.target_ip))
        pending = asyncio.Task.all_tasks()  # allow end the last task!
        loop.run_until_complete(asyncio.gather(*pending))
        
        
    async def download(self, url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                content = await response.content.read() 
                del content

if __name__ == "__main__":
    print("multiple request")
    parser = argparse.ArgumentParser(description="Arguments to work with")
    parser.add_argument('--target_ip', default="localhost", help='destination ip')
    parser.add_argument('--target_port', default="7079", help='destination ip')
    args = parser.parse_args()
    MultipleRequest(args.target_ip, args.target_port)