from ubuntu:trusty
RUN apt-get -y update; \
    apt-get -y install apt-utils \
    vim \
    htop;
RUN sudo apt-get upgrade
RUN sudo apt-get install python3.7
RUN apt-get -y install python3-pip
RUN apt-get -y install iperf
RUN apt-get -y install tcpdump
RUN apt-get -y install tshark
RUN apt-get -y install sysbench
CMD ["bash"]

# sudo apt install python3-pip
# apt-get install software-properties-common
# apt-get install -y software-properties-common
# sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.4 1
# sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.6 2
# sudo update-alternatives --config python3
# wget https://bootstrap.pypa.io/ez_setup.py -O - | python3
# sudo apt-get install python-dev
# sudo apt-get install vim
import asyncio
import websockets

async def hello(websocket, path):
    name = await websocket.recv()
    print(f"< {name}")

    greeting = f"Hello {name}!"

    await websocket.send(greeting)
    print(f"> {greeting}")

start_server = websockets.serve(hello, "172.17.0.3", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()