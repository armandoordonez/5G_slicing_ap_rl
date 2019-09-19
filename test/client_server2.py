import asyncio
import argparse
import aiohttp
import gc
class MultipleRequest():
    def __init__(self, target_ip, target_port):
        self.target_ip = "http://"+target_ip + ":" + target_port
        print("target ip: {}".format(self.target_ip))    
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.start())



    async def start(self):
        while True:
            print("starting new loop")
            gather_vector = []
            for _ in range(55): # 55 
                gather_vector.append(self.download(self.target_ip))
            results = await asyncio.gather(*gather_vector)
            await asyncio.sleep(3)
            print(results)
            gc.collect()
            #await asyncio.gather(*gather_vector)

    async def download(self, url):
        print("download...")
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                await response.content.read() 
                response.close()
                print("download finished....")
            await session.close()
        return 200

    async def stream(self, url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                response.content
                print("streaming...")

                
if __name__ == "__main__":
    print("multiple request")
    parser = argparse.ArgumentParser(description="Arguments to work with")
    parser.add_argument('--target_ip', default="localhost", help='destination ip')
    parser.add_argument('--target_port', default="7079", help='destination ip')
    args = parser.parse_args()
    MultipleRequest(args.target_ip, args.target_port)