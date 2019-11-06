FROM ubuntu:18.04
RUN apt-get update
RUN apt-get install -y python3
RUN apt install -y python3-pip
RUN pip3 install  aiohttp
COPY video.mp4 /home
COPY server.py /home