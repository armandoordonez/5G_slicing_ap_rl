import asyncio
import argparse
import aiohttp
#import gc
class MultipleRequest():
    def __init__(self, target_ip, target_port):
        self.target_ip = "http://"+target_ip + ":" + target_port
        print("target ip: {}".format(self.target_ip))    
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.set_clients())

    async def start(self):
        while True:
            print("starting new loop")
            gather_vector = []

            for counter in range(1): # 55 

                gather_vector.append(self.main(counter = counter))
            await asyncio.gather(*gather_vector)
            await asyncio.sleep(3)
            
            #gc.collect()
            #await asyncio.gather(*gather_vector)
    async def set_clients(self):
        print("starting new loop")
        gather_vector = []
        for counter in range(100): # 55 
            gather_vector.append(self.client(counter = counter))
        await asyncio.gather(*gather_vector)
        print("ending loop...")
        await asyncio.sleep(3)
    async def client(self, counter):
        async with aiohttp.ClientSession() as session:
            while True:
                print("#{} requesting... ".format(counter))
                html = await self.fetch(session, self.target_ip)
                print(html)
                #await asyncio.sleep(2)

    async def fetch(self, session, url):
        async with session.get(url) as response:
            return await response.text()

    async def main(self, counter):
        async with aiohttp.ClientSession() as session:
            print("request #{}".format(counter))
            html = await self.fetch(session, self.target_ip)
            #print()
        await self.main(counter)

    async def download(self, url):
        print("download...")
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                await response.content.read() 
                response.close()
                print("download finished....")

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