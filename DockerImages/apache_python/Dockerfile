FROM ubuntu:18.04
RUN apt-get update
RUN apt-get install -y python3
RUN apt install -y python3-pip
RUN pip3 install  aiohttp
COPY video.mp4 /home
COPY server.py /home
RUN nohup python3 /home/server.py > /home/server.log 2>&1&