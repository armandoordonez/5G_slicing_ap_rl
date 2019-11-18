import asyncio
import argparse
import aiohttp
import logging
class MultipleRequest():
    def __init__(self, target_ip, target_port, clients, interval, debug, filename):
        logging.info("q parezca fiestaas")
        self.target_ip = "http://"+target_ip + ":" + target_port
        self.clients = clients
        self.interval = interval
        self.debug = debug
        self.filename = filename
        self.custom_print("target ip: {}".format(self.target_ip))    
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.set_clients())

    async def set_clients(self):
        self.custom_print("starting new loop")
        gather_vector = []
        for counter in range(self.clients): # 55 
            gather_vector.append(self.client(counter = counter))
        await asyncio.gather(*gather_vector)
        self.custom_print("ending loop...")
        await asyncio.sleep(3)

    # :7079/downloads/video.mp4
    # :7079/calculate
    async def client(self, counter):
        async with aiohttp.ClientSession() as session:
            while True:
                self.custom_print("#{} requesting... ".format(counter))
                html = await self.fetch(session, self.target_ip+"/calculate") #calculate....
                self.custom_print("#{} downloading {}... ".format(counter, self.filename))
                #await self.fetch(session, self.target_ip+"/download/"+self.filename) #download....
                self.custom_print("#{} downloaded... ".format(counter))
                self.custom_print("#{} response: {}".format(counter, html))
                await asyncio.sleep(self.interval)

    async def fetch(self, session, url):
        async with session.get(url) as response:
            return await response.text()

    def custom_print(self, string):
        if self.debug:
            print(string)

                
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Arguments to work with")
    parser.add_argument('--target_ip', default="localhost", help='destination ip')
    parser.add_argument('--target_port', default="7079", help='destination ip')
    parser.add_argument('--filename', default="video.mp4", help='Filename to download')
    parser.add_argument('--clients', default="100", help='How many clients do you want')
    parser.add_argument('--interval', default="0", help='Number of seconds between each requests')
    parser.add_argument('--debug', default=False, help='If you wanna some help..')
    args = parser.parse_args()
    MultipleRequest(args.target_ip, args.target_port, int(args.clients), int(args.interval), args.debug, args.filename)


#todo: delete the download option....