import asyncio
from itertools import cycle

class MainClass():
    def __init__(self):
        loop = asyncio.get_event_loop()

        asyncio.ensure_future(self.counter("anuel"))
        my_tasks = []
        asyncio.ensure_future(self.add_tasks())
        """
        asyncio.ensure_future(self.counter("ozuna"))
        asyncio.ensure_future(self.printer())
        asyncio.ensure_future(self.cancel_counters())
        """


        
        pending = asyncio.Task.all_tasks()
        print("main pending tasks: {}".format(len(pending)))        
        loop.run_until_complete(asyncio.gather(*pending))
    
    async def add_tasks(self):
        counter = 0
        while True:
            loop = asyncio.get_event_loop()
            pending = asyncio.Task.all_tasks()
            print("pending tasks: {}".format(len(pending)))  
            await asyncio.sleep(5)  
            asyncio.ensure_future(self.counter("{} 6ixnin9".format(counter)))
            counter += 1
            #loop.run_until_complete(asyncio.gather(*pending))


    async def counter(self, tag):
        counter = 0
        try:
            while True:
                counter += 1
                print("counter {} tag{}".format(counter, tag))
                await asyncio.sleep(1)
        except asyncio.CancelledError as e:
            print("Task cancelled!")
    async def printer(self):
        counter = 0
        phrase = "HablamePapi"

        loop = cycle(phrase)
        
        for palabra in loop:
            print("printer: {}".format(palabra))
            await asyncio.sleep(0.9)
            counter += 1

    async def cancel_counters(self):
        await asyncio.sleep(5)
        pending = asyncio.Task.all_tasks()
        print(type(pending))
        for task in pending:
            print(type(task))
            print(str(task))
            if "MainClass.counter()" in str(str(task)):
                print("hola") 
                task.cancel()


MainClass()
